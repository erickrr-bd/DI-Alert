from threading import Thread
from datetime import datetime
from libPyLog import libPyLog
from libPyElk import libPyElk
from time import sleep, strftime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram

"""
Class that manages everything related to DI-Alert.
"""
class DIAlert:

	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__telegram = libPyTelegram()
		self.__elasticsearch = libPyElk()


	def startDIAlert(self):
		"""
		Method that starts the application.
		"""
		self.__logger.generateApplicationLog("DI-Alert v3.1", 1, "__start", use_stream_handler = True)
		self.__logger.generateApplicationLog("@2022 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
		self.__logger.generateApplicationLog("Author: Erick Rodriguez", 1, "__start", use_stream_handler = True)
		self.__logger.generateApplicationLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1, "__start", use_stream_handler = True)
		self.__logger.generateApplicationLog("License: GPLv3", 1, "__start", use_stream_handler = True)
		self.__logger.generateApplicationLog("DI-Alert started", 1, "__start", use_stream_handler = True)
		try:
			di_alert_data = self.__utils.readYamlFile(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			self.__logger.generateApplicationLog("Configuration file found in: " + self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE, 1, "__readConfigurationFile", use_stream_handler = True)
			if di_alert_data["use_authentication_method"] == True:
				if di_alert_data["authentication_method"] == "API Key":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchAPIKey(di_alert_data, self.__constants.PATH_KEY_FILE)
				elif di_alert_data["authentication_method"] == "HTTP Authentication":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchHTTPAuthentication(di_alert_data, self.__constants.PATH_KEY_FILE)
			else:
				conn_es = self.__elasticsearch.createConnectionToElasticSearchWithoutAuthentication(di_alert_data)
			self.__logger.generateApplicationLog("Established connection with: " + ",".join(di_alert_data['es_host']) + " Port: " + str(di_alert_data['es_port']), 1, "__connection" , use_stream_handler = True)
			self.__logger.generateApplicationLog("Elasticsearch Cluster Name: " + conn_es.info()["cluster_name"], 1, "__connection", use_stream_handler = True)
			self.__logger.generateApplicationLog("Elasticsearch Version: " + conn_es.info()["version"]["number"], 1, "__connection", use_stream_handler = True)
			time_execution = di_alert_data["time_execution"].split(':')
			for index_pattern in di_alert_data["index_pattern_es"]:
				self.__logger.generateApplicationLog("Index pattern load.", 1, "__" + index_pattern, use_stream_handler = True)
				Thread(name = index_pattern, target = self.__startIndexPatternValidator, args = (conn_es, index_pattern, time_execution, )).start()
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__logger.generateApplicationLog("Error to encrypt or decrypt the data. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, OSError, IOError) as exception:
			self.__logger.generateApplicationLog("Error when executing an action on a file or folder. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (self.__elasticsearch.exceptions.AuthenticationException, self.__elasticsearch.exceptions.ConnectionError, self.__elasticsearch.exceptions.AuthorizationException, self.__elasticsearch.exceptions.RequestError, self.__elasticsearch.exceptions.ConnectionTimeout, self.__elasticsearch.exceptions.TransportError) as exception:
			self.__logger.generateApplicationLog("Error connecting with ElasticSearch. For more information, see the logs.", 3, "__connection", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__connection", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)


	def __startIndexPatternValidator(self, conn_es, index_pattern_name, time_execution):
		"""
		Method that performs the search for version changes of the documents of a specific index pattern.

		:arg conn_es (object): Object that contains a connection to ElasticSearch.
		:arg index_pattern_name (string): Index pattern's name.
		:arg time_execution (array): Time of execution of the data integrity validation.
		"""
		while True:
			now = datetime.now()
			if now.hour == int(time_execution[0]) and now.minute == int(time_execution[1]):
				list_documents_version_changes = self.__elasticsearch.getDocumentsVersionChangeinIndexPattern(conn_es, index_pattern_name, "now-7d/d", "now/d")
				if list_documents_version_changes:
					self.__logger.generateApplicationLog("Changes were found in the index pattern's documents", 1, "__" + index_pattern_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
					for document in list_documents_version_changes:
						message_telegram = self.__generateTelegramMessage(document)
						response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
						self.__createLogByTelegramCode(response_http_code)
				else:
					self.__logger.generateApplicationLog("No changes were found in the index pattern's documents", 1, "__" + index_pattern_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
			sleep(60)


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


	def __createLogByTelegramCode(self, response_http_code, index_pattern_name):
		"""
		Method that creates a log based on the Telegram's HTTP Code received as a response.

		:arg response_http_code (integer): HTTP code received in the response when sending the alert to Telegram.
		:arg index_pattern_name (string): Index pattern's name.
		"""
		if response_http_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__" + index_pattern_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__" + index_pattern_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__" + index_pattern_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__" + index_pattern_name, use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)