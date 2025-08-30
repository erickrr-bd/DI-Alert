"""
Class that manages the validation of index's integrity.
"""
from os import path
from time import strftime
from libPyElk import libPyElk
from libPyLog import libPyLog
from dataclasses import dataclass
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from libPyConfiguration import libPyConfiguration

@dataclass
class IndexValidator:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()
		self.telegram = libPyTelegram()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def index_validator(self) -> None:
		"""
		Method that validates a specific index's integrity.
		"""
		try:
			if path.exists(self.constants.ES_CONFIGURATION):
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
				indexes = self.elasticsearch.get_indexes(conn_es)
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(indexes, "Index Name")
				index = self.dialog.create_radiolist("Select a option:", 17, 70, tuple_to_rc, "Indexes")
				documents = self.elasticsearch.validate_index_integrity(conn_es, index)
				documents = [sublist for sublist in documents if sublist]
				if documents:
					if path.exists(self.constants.DI_ALERT_CONFIGURATION):
						di_alert_data = self.utils.read_yaml_file(self.constants.DI_ALERT_CONFIGURATION)
						for document in documents:
							self.send_telegram_message(di_alert_data, document)
					else:
						self.dialog.create_message("\nConfiguration not found", 7, 50, "Error Message")
					self.dialog.create_message(f"\nModified documents were found in the index: {index}", 8, 50, "Notification Message")
					self.logger.create_log(f"\nModified documents were found in the index: {index}", 2, "_indexValidation", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				else:
					self.dialog.create_message(f"\nNo modified documents found in the index: {index}", 8, 50, "Notification Message")
					self.logger.create_log(f"\nNo modified documents found in the index: {index}", 2, "_indexValidation", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			else:
				self.dialog.create_message("\nES Configuration not found", 7, 50, "Error Message")
		except Exception as exception:
			self.dialog.create_message("\nError validating index integrity. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_indexValidation", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def send_telegram_message(self, di_alert_data: dict, document: list) -> None:
		"""
		Method that sends an alert to a Telegram channel.

		Parameters:
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
		self.create_log_by_telegram_code(response_http_code)


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


	def create_log_by_telegram_code(self, response_http_code: int) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
