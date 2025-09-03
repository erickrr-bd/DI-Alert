"""
Class that manages the DI-Alert-Agent's operation.
"""
from os import path
from libPyLog import libPyLog
from time import sleep, strftime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from dataclasses import dataclass, field
from apscheduler.schedulers.background import BackgroundScheduler

@dataclass
class DIAlertAgent:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.telegram = libPyTelegram()
		self.scheduler = BackgroundScheduler()
		self.scheduler.start()


	def run_as_daemon(self) -> None:
		"""
		Method that runs the application as a daemon.
		"""
		try:
			self.start_di_alert_agent()
			while True:
				sleep(60)
		except (KeyboardInterrupt, SystemExit)  as exception:
			self.scheduler.shutdown()
			self.logger.create_log("DI-Alert-Agent daemon stopped", 2, "_daemon", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_di_alert_agent(self) -> None:
		"""
		Method that starts DI-Alert-Agent.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/DI-Alert", 2, "_start", use_stream_handler = True)
			self.logger.create_log("DI-Alert-Agent v3.2 - September 2025", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.DI_ALERT_AGENT_CONFIGURATION):
				self.logger.create_log(f"Configuration found: {self.constants.DI_ALERT_AGENT_CONFIGURATION}", 2, "_readConfiguration", use_stream_handler = True)
				di_alert_agent_data = self.utils.read_yaml_file(self.constants.DI_ALERT_AGENT_CONFIGURATION)
				self.start_daemon_validation(di_alert_agent_data)
			else:
				self.logger.create_log("Configuration not found.", 4, "_readConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error starting DI-Alert-Agent. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_start", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_daemon_validation(self, di_alert_agent_data: dict) -> None:
		"""
		Method that executes a task in a defined time interval.

		Parameters:
			di_alert_agent_data (dict): Object that contains the DI-Alert-Agent's configuration data.
		"""
		unit_time = list(di_alert_agent_data["frequency_time"].keys())[0]
		frequency_time = di_alert_agent_data["frequency_time"][unit_time]
		interval_args = {unit_time : frequency_time}
		self.scheduler.add_job(self.daemon_validator, "interval", **interval_args, args = [di_alert_agent_data], id = "daemon_validation", replace_existing = True)


	def daemon_validator(self, di_alert_agent_data: dict) -> None:
		"""
		Method that validates the status of the DI-Alert's daemon.

		Parameters:
			di_alert_agent_data (dict): Object that contains the DI-Alert-Agent's configuration data.
		"""
		try:
			di_alert_status = self.utils.get_status_by_daemon("di-alert.service")
			self.logger.create_log(f"DI-Alert service status: {di_alert_status}", 2, "_statusService", use_stream_handler = True)
			if di_alert_status == "Not running":
				passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
				telegram_bot_token = self.utils.decrypt_data(di_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
				telegram_chat_id = self.utils.decrypt_data(di_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
				telegram_message = self.generate_telegram_message()
				response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
				self.create_log_by_telegram_code(response_http_code)
				result = self.utils.manage_daemon("di-alert.service", 1)
				if result == 0:
					self.logger.create_log("DI-Alert service has been started", 3, "_statusService", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.logger.create_log("Error validating DI-Alert status. For more information, see the logs.", 4, "_statusService", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_statusService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def generate_telegram_message(self) -> str:
		"""
		Method that generates the message to be sent via Telegram when the service isn't working.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{u'\u26A0\uFE0F'} DI-Alert Service {u'\u26A0\uFE0F'}\n\n{u'\u23F0'} Service Status Validation Time: {strftime("%c")}\n\n\n"
		telegram_message += "DI-Alert Service Status: 🔴\n\n"
		telegram_message += f"{u'\U0001f4cb'} NOTE: The red circle indicates that DI-Alert service isn't working. Report to an administrator.\n\n"
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code: int) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, "_sendTelegramMessage", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
