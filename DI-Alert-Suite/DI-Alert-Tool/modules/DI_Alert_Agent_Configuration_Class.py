from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the DI-Alert-Agent configuration.
"""
class DIAlertAgentConfiguration:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def createConfiguration(self):
		"""
		Method that creates the DI-Alert-Agent configuration.
		"""
		di_alert_agent_data = []
		try:
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			first_execution_time = self.__dialog.createTimeDialog("Select the first time of service validation:", 2, 50, -1, -1)
			di_alert_agent_data.append(str(first_execution_time[0]) + ':' + str(first_execution_time[1]))
			second_execution_time = self.__dialog.createTimeDialog("Select the second time of service validation:", 2, 50, -1, -1)
			di_alert_agent_data.append(str(second_execution_time[0]) + ':' + str(second_execution_time[1]))
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			di_alert_agent_data.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			di_alert_agent_data.append(telegram_chat_id.decode("utf-8"))
			self.__createConfigurationYamlFile(di_alert_agent_data)
			if path.exists(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE):
				self.__dialog.createMessageDialog("\nDI-Alert-Agent configuration file created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("DI-Alert-Agent configuration file created", 1, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nError to encrypt or decrypt the data. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, IOError, OSError) as exception:
			self.__dialog.createMessageDialog("\nError when executing an action on a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def modifyConfiguration(self):
		"""
		Method that allows to modify one or more values in the DI-Alert-Agent configuration file.
		"""
		try:
			di_alert_agent_data = self.__utils.readYamlFile(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
			options_di_alert_agent_update = self.__dialog.createCheckListDialog("Select one or more options:", 11, 65, self.__constants.OPTIONS_DI_ALERT_AGENT_UPDATE, "DI-Alert-Agent Configuration Update")
			if "First Execution" in options_di_alert_agent_update:
				actual_first_execution_time = di_alert_agent_data["first_execution_time"].split(':')
				first_execution_time = self.__dialog.createTimeDialog("Select the first time of service validation:", 2, 50, int(actual_first_execution_time[0]), int(actual_first_execution_time[1]))
				di_alert_agent_data["first_execution_time"] = str(first_execution_time[0]) + ':' + str(first_execution_time[1])
			if "Second Execution" in options_di_alert_agent_update:
				actual_second_execution_time = di_alert_agent_data["second_execution_time"].split(':')
				second_execution_time = self.__dialog.createTimeDialog("Select the second time of service validation:", 2, 50, int(actual_second_execution_time[0]), int(actual_second_execution_time[1]))
				di_alert_agent_data["second_execution_time"] = str(di_alert_agent_data[0]) + ':' + str(di_alert_agent_data[1])
			if "Bot Token" in options_di_alert_agent_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.__utils.decryptDataWithAES(di_alert_agent_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
				di_alert_agent_data["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
			if "Chat ID" in options_di_alert_agent_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.__utils.decryptDataWithAES(di_alert_agent_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
				di_alert_agent_data["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
			self.__utils.createYamlFile(di_alert_agent_data, self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
			if hash_file_configuration_original == hash_file_configuration_new:
				self.__dialog.createMessageDialog("\nDI-Alert-Agent configuration file not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nDI-Alert-Agent configuration file modified.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("DI-Alert-Agent configuration file modified", 2, "__modifyAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__modifyAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nError to encrypt or decrypt the data. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__modifyAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, IOError, OSError) as exception:
			self.__dialog.createMessageDialog("\nError when executing an action on a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__modifyAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def showConfigurationData(self):
		"""
		Method that displays the data stored in the DI-Alert-Agent configuration file.
		"""
		try:
			di_alert_agent_data = self.__utils.convertDataYamlFileToString(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
			message_to_display = "\nDI-Alert-Agent Configuration:\n\n" + di_alert_agent_data
			self.__dialog.createScrollBoxDialog(message_to_display, 11, 70, "DI-Alert-Agent Configuration")
		except (IOError, OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError when executing an action on a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showAgentConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def __createConfigurationYamlFile(self, di_alert_agent_data):
		""" 	
		Method that creates the YAML file corresponding to the DI-Alert-Agent configuration.

		:arg di_alert_agent_data: Data to be stored in the configuration file.
		"""
		di_alert_agent_data_json = {
			"first_execution_time": di_alert_agent_data[0],
			"second_execution_time": di_alert_agent_data[1],
			"telegram_bot_token": di_alert_agent_data[2],
			"telegram_chat_id": di_alert_agent_data[3]
		}

		self.__utils.createYamlFile(di_alert_agent_data_json, self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE)
		self.__utils.changeOwnerToPath(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE, self.__constants.USER, self.__constants.GROUP)