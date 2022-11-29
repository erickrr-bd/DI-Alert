from time import strftime
from libPyLog import libPyLog
from libPyElk import libPyElk
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram

"""
Class that manages everything related to the validation of a specific index.
"""
class IndexValidator:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__elasticsearch = libPyElk()
		self.__telegram = libPyTelegram()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def indexValidator(self):
		"""
		Method that validates the integrity of the data of a specific index.
		"""
		try:
			di_alert_data = self.__utils.readYamlFile(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			if di_alert_data["use_authentication_method"] == True:
				if di_alert_data["authentication_method"] == "HTTP Authentication":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchHTTPAuthentication(di_alert_data, self.__constants.PATH_KEY_FILE)
				elif di_alert_data["authentication_method"] == "API Key":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchAPIKey(di_alert_data, self.__constants.PATH_KEY_FILE)
			else:
				conn_es = self.__elasticsearch.createConnectionToElasticSearchWithoutAuthentication(di_alert_data)
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(di_alert_data["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(di_alert_data["telegram_chat_id"], passphrase).decode("utf-8")
			list_all_indexes = self.__elasticsearch.getIndexes(conn_es)
			list_to_dialog = self.__utils.convertListToDialogList(list_all_indexes, "Index Name")
			index_to_validate = self.__dialog.createRadioListDialog("Select a option:", 17, 70, list_to_dialog, "Indexes")
			self.__logger.generateApplicationLog("Index validator started: " + index_to_validate, 1, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			list_documents_version_changes = self.__elasticsearch.getDocumentsVersionChangeinIndex(conn_es, index_to_validate)
			if list_documents_version_changes:
				for document in list_documents_version_changes:
					message_telegram = self.__generateTelegramMessage(document)
					response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
					self.__createLogByTelegramCode(response_http_code)
				self.__dialog.createMessageDialog("\nChanges were found in the index documents:" + index_to_validate, 8, 50, "Notification Message")
				self.__logger.generateApplicationLog("Changes were found in the index documents: " + index_to_validate, 2, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			else:
				self.__dialog.createMessageDialog("\nNo changes were found in the index documents: " + index_to_validate, 8, 50, "Notification Message")
				self.__logger.generateApplicationLog("No changes were found in the index documents: " + index_to_validate, 1, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nError to encrypt or decrypt the data. For more information see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, OSError, IOError) as exception:
			self.__dialog.createMessageDialog("\nError to open, read or write a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError, self.__elasticsearch.exceptions.ConnectionTimeout, self.__elasticsearch.exceptions.TransportError) as exception:
			self.__dialog.createMessageDialog("\nError connecting with ElasticSearch. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__indexValidator", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def __generateTelegramMessage(self, document):
		"""
		Method that generates the Telegram message.

		Return the Telegram message.

		:arg document (list): Object that contains the data of the document.
		"""
		message_telegram = u'\u26A0\uFE0F' + " " + "Data Change" +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\U0001f6a6' +  " Alert level: " + "High" + "\n\n" +  u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n"
		message_telegram += u"\u270F\uFE0F" + " The data of a document has been updated and/or modified.\n\n"
		message_telegram += u"\u2611\uFE0F" + " " + " _index" + " = " + str(document[0]) + "\n"
		message_telegram += u"\u2611\uFE0F" + " " + " _id" + " = " + str(document[1]) + "\n"
		message_telegram += u"\u2611\uFE0F" + " " + " _version" + " = " + str(document[2]) + "\n"
		return message_telegram


	def __createLogByTelegramCode(self, response_http_code):
		"""
		Method that creates a log based on the HTTP code received as a response.

		:arg response_http_code (integer): HTTP code received in the response when sending the alert to Telegram.
		"""
		if response_http_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)