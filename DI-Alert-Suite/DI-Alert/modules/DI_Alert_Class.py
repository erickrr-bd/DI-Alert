"""
Class that manages the operation of DI-Alert.
"""
from os import path
from libPyLog import libPyLog
from libPyElk import libPyElk
from time import strftime, sleep
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from dataclasses import dataclass, field
from libPyConfiguration import libPyConfiguration
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

@dataclass
class DIAlert:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()
		self.telegram = libPyTelegram()
		self.scheduler = BackgroundScheduler()
		self.scheduler.start()


	def run_as_daemon(self) -> None:
		"""
		Method that runs the application as a daemon.
		"""
		try:
			self.start_di_alert()
			while True:
				sleep(60)
		except (KeyboardInterrupt, SystemExit)  as exception:
			self.scheduler.shutdown()
			self.logger.create_log("DI-Alert daemon stopped", 2, "_daemon", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_di_alert(self) -> None:
		"""
		Method that starts DI-Alert.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/DI-Alert", 2, "_start", use_stream_handler = True)
			self.logger.create_log("DI-Alert v3.2 - September 2025", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.ES_CONFIGURATION):
				self.logger.create_log(f"ES Configuration found: {self.constants.ES_CONFIGURATION}", 2, "_readESConfiguration", use_stream_handler = True)
				configuration = libPyConfiguration()
				data = self.utils.read_yaml_file(self.constants.ES_CONFIGURATION)
				configuration.convert_dict_to_object(data)
				if configuration.use_authentication:
					if configuration.authentication_method == "HTTP Authentication":
						conn_es = self.elasticsearch.create_connection_http_auth(configuration, self.constants.KEY_FILE)
					elif configuration.authentication_method == "API Key":
						conn_es = self.elasticsearch.create_connection_api_key(configuration, self.constants.KEY_FILE)
				else:
					conn_es = self.elasticsearch.create_connection_without_auth(configuration)
				self.logger.create_log(f"Connection established: {','.join(configuration.es_host)}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Cluster Name: {conn_es.info()["cluster_name"]}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Cluster UUID: {conn_es.info()["cluster_uuid"]}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Version: {conn_es.info()["version"]["number"]}", 2, "_clusterConnection", use_stream_handler = True)
				if configuration.use_authentication:
					self.logger.create_log("Authentication enabled", 2, "_clusterConnection", use_stream_handler = True)
					self.logger.create_log("Authentication Method: HTTP Authentication", 2, "_clusterConnection", use_stream_handler = True) if configuration.authentication_method == "HTTP Authentication" else self.logger.create_log("Authentication Method: API Key", 2, "_clusterConnection", use_stream_handler = True)
				else:
					self.logger.create_log("Authentication disabled. Not recommended for security reasons.", 3, "_clusterConnection", use_stream_handler = True)
				if configuration.verificate_certificate_ssl:
					self.logger.create_log("SSL Certificate verification enabled", 2, "_clusterConnection", use_stream_handler = True)
					self.logger.create_log(f"SSL Certificate: {configuration.certificate_file}", 2, "_clusterConnection", use_stream_handler = True)
				else:
					self.logger.create_log("SSL Certificate verification disabled. Not recommended for security reasons.", 3, "_clusterConnection", use_stream_handler = True)
				if path.exists(self.constants.DI_ALERT_CONFIGURATION):
					self.logger.create_log(f"DI-Alert Configuration found: {self.constants.DI_ALERT_CONFIGURATION}", 2, "_readConfiguration", use_stream_handler = True)
					di_alert_data = self.utils.read_yaml_file(self.constants.DI_ALERT_CONFIGURATION)
					for index_pattern in di_alert_data["index_pattern"]:
						self.logger.create_log(f"Index Pattern: {index_pattern}", 2, "_loadIndexPattern", use_stream_handler = True)
						self.start_daily_validation(conn_es, index_pattern, di_alert_data)
				else:
					self.logger.create_log("DI-Alert Configuration not found.", 4, "_readConfiguration", use_stream_handler = True)
			else:
				self.logger.create_log("ES Configuration not found.", 4, "_readESConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error starting DI-Alert. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_start", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_daily_validation(self, conn_es, index_pattern: str, di_alert_data: dict) -> None:
		"""
		Method that executes a task at a specific time using a cron.

		Parameters:
			conn_es (ElasticSearch): A straightforward mapping from Python to ES REST endpoints.
			index_pattern (str): Index Pattern to validate.
			di_alert_data (dict): Object that contains the DI-Alert's configuration data.
		"""
		execution_time = di_alert_data["execution_time"].split(':')
		job_id = index_pattern
		trigger = CronTrigger(hour = int(execution_time[0]), minute = int(execution_time[1]))
		self.scheduler.add_job(self.index_pattern_validator, trigger = trigger, args = [conn_es, index_pattern, di_alert_data], id = job_id, replace_existing = True)


	def index_pattern_validator(self, conn_es, index_pattern: str, di_alert_data: dict) -> None:
		"""
		MMethod that validates the integrity of Index Pattern's documents in a defined time range.

		Parameters:
			conn_es (ElasticSearch): A straightforward mapping from Python to ES REST endpoints.
			index_pattern (str): Index Pattern to validate.
			di_alert_data (dict): Object that contains the DI-Alert's configuration data.
		"""
		try:
			unit_time = list(di_alert_data["range_time"].keys())[0]
			gte = self.utils.get_gte_date(unit_time, di_alert_data["range_time"][unit_time])
			lte = self.utils.get_lte_date(unit_time)
			self.logger.create_log("Validation started", 2, f"_{index_pattern}", use_stream_handler = True)
			documents = self.elasticsearch.validate_index_pattern_integrity(conn_es, index_pattern, di_alert_data["timestamp_field"], gte, lte)
			documents = [sublist for sublist in documents if sublist]
			if documents:
				for document in documents:
					self.send_telegram_message(index_pattern, di_alert_data, document)
				self.logger.create_log(f"\nModified documents were found in the Index Pattern: {index_pattern}", 2, "_indexPatternValidation", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			else:
				self.logger.create_log(f"\nNo modified documents found in the Index Pattern: {index_pattern}", 2, "_indexPatternValidation", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.logger.create_log("Error running the job. For more information, see the logs.", 4, f"_{index_pattern}", use_stream_handler = True)
			self.logger.create_log(exception, 4, f"_{index_pattern}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def send_telegram_message(self, index_pattern: str, di_alert_data: dict, document: list) -> None:
		"""
		Method that sends an alert to a Telegram channel.

		Parameters:
			index_pattern (str): Index Pattern to validate.
			di_alert_data (dict): Object that contains the DI-Alert's configuration data.
			document (list): List containing the data of the modified document.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		telegram_bot_token = self.utils.decrypt_data(di_alert_data["telegram_bot_token"], passphrase).decode("utf-8")
		telegram_chat_id = self.utils.decrypt_data(di_alert_data["telegram_chat_id"], passphrase).decode("utf-8")
		telegram_message = self.generate_telegram_message(document)
		if len(telegram_message) > 4096:
			telegram_message = f"{u'\u26A0\uFE0F'} DI-Alert {u'\u26A0\uFE0F'}\n\n{u'\u270F\uFE0F'} The size of the message in Telegram (4096) has been exceeded. Overall size: {str(len(telegram_message))}"
		response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
		self.create_log_by_telegram_code(response_http_code, index_pattern)


	def generate_telegram_message(self, document: list) -> str:
		"""
		Method that generates the message to be sent via Telegram.

		Parameters:
			document (list): List of modified or altered documents.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{u'\u26A0\uFE0F'} DI-Alert {u'\u26A0\uFE0F'}\n\n{u'\U0001f6a6'} Alert level: High\n\n{u'\u23F0'} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{u'\u270F\uFE0F'} Modified documents were found. Index's integrity is compromised.\n\n"
		telegram_message += f"{u'\u2611\uFE0F'} _index = {document[0]}\n"
		telegram_message += f"{u'\u2611\uFE0F'} _id = {document[1]}\n"
		telegram_message += f"{u'\u2611\uFE0F'} _version = {document[2]}\n"
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code: int, index_pattern : str) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
			index_pattern (str): Index Pattern's name.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, f"_{index_pattern}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, f"_{index_pattern}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, f"_{index_pattern}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, f"_{index_pattern}", use_stream_handler = True, use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
