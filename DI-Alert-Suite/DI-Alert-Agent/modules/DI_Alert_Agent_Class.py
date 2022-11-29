from os import popen
from datetime import datetime
from libPyLog import libPyLog
from time import sleep,strftime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram

"""
Class that manages the operation of DI-Alert-Agent.
"""
class DIAlertAgent:

	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__telegram = libPyTelegram()


	def startDIAlertAgent(self):
		"""
		Method that starts the DI-Alert-Agent application.
		"""
		try:
			di_alert_agent_data = self.__utils.readYamlFile(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
			first_execution_time = di_alert_agent_data["first_execution_time"].split(':')
			second_execution_time = di_alert_agent_data["second_execution_time"].split(':')
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(di_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(di_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")
			self.__logger.generateApplicationLog("DI-Alert-Agent v3.1", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("@2022 Tekium. All rights reserved.", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("Author: Erick Rodriguez", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("License: GPLv3", 1, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog("DI-Alert-Agent started", 1, "__start", use_stream_handler = True)
			while True:
				result_comand_line = popen('(systemctl is-active --quiet di-alert.service && echo "Running" || echo "Not running")')
				result_comand_line_aux = result_comand_line.readlines()
				for line in result_comand_line_aux:
					di_alert_service_status = line.rstrip('\n')
				if di_alert_service_status == "Not running":
					message_telegram = self.__generateTelegramMessage(di_alert_service_status)
					response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
					self.__createLogByTelegramCode(response_http_code)
				else:
					now = datetime.now()
					if(now.hour == int(first_execution_time[0]) and now.minute == int(first_execution_time[1])) or (now.hour == int(second_execution_time[0]) and now.minute == int(second_execution_time[1])):
						message_telegram = self.__generateTelegramMessage(di_alert_service_status)
						response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
						self.__createLogByTelegramCode(response_http_code)
				self.__logger.generateApplicationLog("DI-Alert service status: " + di_alert_service_status, 1, "__serviceValidation", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
				sleep(60)
		except KeyError as exception:
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__logger.generateApplicationLog("Error to encrypt or decrypt the data. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (OSError, FileNotFoundError, IOError) as exception:
			self.__logger.generateApplicationLog("Error when executing an action on a file or folder. For more information, see the logs.", 3, "__start", use_stream_handler = True)
			self.__logger.generateApplicationLog(exception, 3, "__start", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)


	def __generateTelegramMessage(self, di_alert_service_status):
		"""
		Method that generates the Telegram message based on the current state of the DI-Alert service.

		Returns the Telegram message formed.

		:arg di_alert_service_status (string): Current state of the DI-Alert service.
		"""
		message_telegram = "" + u'\u26A0\uFE0F' + "DI-Alert Service " + u'\u26A0\uFE0F' + '\n\n' + u'\u23F0' + "Service Status Validation Time: " + strftime("%c") + "\n\n\n"
		if di_alert_service_status == "Not running":
			message_telegram += "Service DI-Alert Status: " + u'\U0001f534' + "\n\n"
		elif di_alert_service_status == "Running":
			message_telegram += "Service DI-Alert Status: " + u'\U0001f7e2' + "\n\n"
		message_telegram += "" + u'\U0001f4cb' + " " + "Note 1: The green circle indicates that the DI-Alert service is working without problems." + "\n\n"
		message_telegram += "" + u'\U0001f4cb' + " " + "Note 2: The red circle indicates that the DI-Alert service is not working. Report to an administrator." + "\n\n"
		return message_telegram


	def __createLogByTelegramCode(self, response_http_code):
		"""
		Method that creates a log based on the HTTP code received as a response.

		:arg response_http_code (integer): HTTP code received in the response when sending the alert to Telegram.
		"""
		if response_http_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif response_http_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__sendTelegramMessage", use_stream_handler = True, use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)