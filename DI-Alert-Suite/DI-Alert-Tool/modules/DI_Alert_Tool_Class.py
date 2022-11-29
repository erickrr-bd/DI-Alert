from os import path
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Index_Validator_Class import IndexValidator
from .DI_Alert_Service_Class import DIAlertService
from .DI_Alert_Agent_Service_Class import DIAlertAgentService
from .DI_Alert_Configuration_Class import DIAlertConfiguration
from .DI_Alert_Agent_Configuration_Class import DIAlertAgentConfiguration

"""
Class that manages what is related to the interfaces and actions of DI-Alert-Tool.
"""
class DIAlertTool:

	def __init__(self):
		"""
		Method that corresponds to the constructor of the class.
		"""
		self.__constants = Constants()
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, self.mainMenu)


	def mainMenu(self):
		"""
		Method that shows the "Main" menu.
		"""
		option_main_menu = self.__dialog.createMenuDialog("Select a option:", 13, 50, self.__constants.OPTIONS_MAIN_MENU, "Main Menu")
		self.__switchMainMenu(int(option_main_menu))


	def __serviceMenu(self):
		"""
		Method that shows the "DI-Alert Service" menu.
		"""
		option_service_menu = self.__dialog.createMenuDialog("Select a option:", 11, 50, self.__constants.OPTIONS_SERVICE_MENU, "DI-Alert Service Menu")
		self.__switchServiceMenu(int(option_service_menu))


	def __diAlertAgentMenu(self):
		"""
		Method that shows the "DI-Alert-Agent" menu.
		"""
		option_di_alert_agent_menu = self.__dialog.createMenuDialog("Select a option:", 9, 50, self.__constants.OPTIONS_DI_ALERT_AGENT_MENU, "DI-Alert-Agent Menu")
		self.__switchDIAlertAgentMenu(int(option_di_alert_agent_menu))


	def __serviceAgentMenu(self):
		"""
		Method that shows the "DI-Alert-Agent Service" menu.
		"""
		option_agent_service_menu = self.__dialog.createMenuDialog("Select a option:", 11, 50, self.__constants.OPTIONS_SERVICE_MENU, "DI-Alert-Agent Service Menu")
		self.__switchAgentServiceMenu(int(option_agent_service_menu))


	def __switchMainMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Main" menu.

		:arg option (integer): Option number.
		"""
		if option == 1:
			self.__defineConfiguration()
		elif option == 2:
			self.__serviceMenu()
		elif option == 3:
			self.__diAlertAgentMenu()
		elif option == 4:
			index_validator = IndexValidator(self.mainMenu)
			index_validator.indexValidator()
		elif option == 5:
			self.__showApplicationAbout()
		elif option == 6:
			exit(1)


	def __switchServiceMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "DI-Alert Service" menu.

		:arg option (integer): Option number.
		"""
		di_alert_service = DIAlertService(self.mainMenu)
		if option == 1:
			di_alert_service.startService()
		elif option == 2:
			di_alert_service.restartService()
		elif option == 3:
			di_alert_service.stopService()
		elif option == 4:
			di_alert_service.getActualStatusService()


	def __switchDIAlertAgentMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "DI-Alert-Agent" menu.

		:arg option (integer): Option number.
		"""
		if option == 1:
			self.__defineAgentConfiguration()
		elif option == 2:
			self.__serviceAgentMenu()


	def __switchAgentServiceMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "DI-Alert-Agent Service" menu.

		:arg option (integer): Option number.
		"""
		di_alert_agent_service = DIAlertAgentService(self.mainMenu)
		if option == 1:
			di_alert_agent_service.startService()
		elif option == 2:
			di_alert_agent_service.restartService()
		elif option == 3:
			di_alert_agent_service.stopService()
		elif option == 4:
			di_alert_agent_service.getActualStatusService()


	def __defineConfiguration(self):
		"""
		Method that defines the action to perform on the DI-Alert configuration (create or modify).
		"""
		di_alert_configuration = DIAlertConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "DI-Alert Configuration Options")
			if option_configuration_false == "Create":
				di_alert_configuration.createConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "DI-Alert Configuration Options")
			if option_configuration_true == "Modify":
				di_alert_configuration.modifyConfiguration()
			elif option_configuration_true == "Show":
				di_alert_configuration.showConfigurationData()


	def __defineAgentConfiguration(self):
		"""
		Method that defines the action to perform on the DI-Alert-Agent configuration (create or modify).
		"""
		di_alert_agent_configuration = DIAlertAgentConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_DI_ALERT_AGENT_CONFIGURATION_FILE):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "DI-Alert-Agent Configuration Options")
			if option_configuration_false == "Create":
				di_alert_agent_configuration.createConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "DI-Alert-Agent Configuration Options")
			if option_configuration_true == "Modify":
				di_alert_agent_configuration.modifyConfiguration()
			elif option_configuration_true == "Show":
				di_alert_agent_configuration.showConfigurationData()


	def __showApplicationAbout(self):
		"""
		Method that shows the "About" of the application.
		"""
		message_to_show = "\nCopyright@2022 Tekium. All rights reserved.\nDI-Alert v3.1\nAuthor: Erick Rodriguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nEasy monitoring and alerting of data integrity in ElasticSearch."
		self.__dialog.createScrollBoxDialog(message_to_show, 13, 70, "About")