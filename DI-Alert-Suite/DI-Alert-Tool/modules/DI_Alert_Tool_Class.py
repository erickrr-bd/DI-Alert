"""
Class that manages everything related to DI-Alert-Tool.
"""
from os import path
from sys import exit
from libPyLog import libPyLog
from dataclasses import dataclass
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Configuration_Class import Configuration
from .Index_Validator_Class import IndexValidator
from libPyConfiguration import libPyConfiguration
from libPyAgentConfiguration import libPyAgentConfiguration

@dataclass
class DIAlertTool:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def main_menu(self) -> None:
		"""
		Main menu.
		"""
		try:
			option = self.dialog.create_menu("Select a option:", 13, 50, self.constants.MAIN_MENU_OPTIONS, "Main Menu")
			self.switch_main_menu(int(option))
		except KeyboardInterrupt:
			pass


	def configuration_menu(self) -> None:
		"""
		Configuration menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.CONFIGURATION_MENU_OPTIONS, "Configuration Menu")
		self.switch_configuration_menu(int(option))


	def service_menu(self) -> None:
		"""
		Service menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.CONFIGURATION_MENU_OPTIONS, "Service Menu")
		self.switch_service_menu(int(option))


	def di_alert_service_menu(self) -> None:
		"""
		DI-Alert service menu.
		"""
		option = self.dialog.create_menu("Select a option:", 11, 50, self.constants.SERVICE_MENU_OPTIONS, "DI-Alert Service Menu")
		self.switch_di_alert_service_menu(int(option))


	def di_alert_agent_service_menu(self) -> None:
		"""
		DI-Alert-Agent service menu.
		"""
		option = self.dialog.create_menu("Select a option:", 11, 50, self.constants.SERVICE_MENU_OPTIONS, "DI-Alert-Agent Service Menu")
		self.switch_di_alert_agent_service_menu(int(option))


	def switch_main_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Main" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				self.define_es_configuration()
			case 2:
				self.configuration_menu()
			case 3:
				index_validator = IndexValidator()
				index_validator.index_validator()
			case 4:
				self.service_menu()
			case 5:
				self.display_about()
			case 6:
				exit(1)


	def switch_configuration_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Configuration" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		self.define_configuration() if option == 1 else self.define_agent_configuration()


	def switch_service_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Service" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		self.di_alert_service_menu() if option == 1 else self.di_alert_agent_service_menu()


	def switch_di_alert_service_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "DI-Alert Service" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				result = self.utils.manage_daemon("di-alert.service", 1)
				if result == 0:
					self.dialog.create_message("\nDI-Alert service started.", 7, 50, "Notification Message")
					self.logger.create_log("DI-Alert service started", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 2:
				result = self.utils.manage_daemon("di-alert.service", 2)
				if result == 0:
					self.dialog.create_message("\nDI-Alert service restarted.", 7, 50, "Notification Message")
					self.logger.create_log("DI-Alert service restarted", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 3:
				result = self.utils.manage_daemon("di-alert.service", 3)
				if result == 0:
					self.dialog.create_message("\nDI-Alert service stopped.", 7, 50, "Notification Message")
					self.logger.create_log("DI-Alert service stopped", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 4:
				service_status = self.utils.get_detailed_status_by_daemon("di-alert.service", "/tmp/di_alert.status")
				self.dialog.create_scrollbox(service_status, 18, 70, "DI-Alert Service")


	def switch_di_alert_agent_service_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "DI-Alert-Agent Service" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				result = self.utils.manage_daemon("di-alert-agent.service", 1)
				if result == 0:
					self.dialog.create_message("\nDI-Alert-Agent service started.", 7, 50, "Notification Message")
					self.logger.create_log("DI-Alert-Agent service started", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 2:
				result = self.utils.manage_daemon("di-alert-agent.service", 2)
				if result == 0:
					self.dialog.create_message("\nDI-Alert-Agent service restarted.", 7, 50, "Notification Message")
					self.logger.create_log("DI-Alert-Agent service restarted", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 3:
				result = self.utils.manage_daemon("di-alert-agent.service", 3)
				if result == 0:
					self.dialog.create_message("\nDI-Alert-Agent service stopped.", 7, 50, "Notification Message")
					self.logger.create_log("DI-Alert-Agent service stopped", 2, "_manageService", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 4:
				service_status = self.utils.get_detailed_status_by_daemon("di-alert-agent.service", "/tmp/di_alert_agent.status")
				self.dialog.create_scrollbox(service_status, 18, 70, "DI-Alert-Agent Service")


	def define_es_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the ElasticSearch connection's configuration with DI-Alert.
		"""
		if not path.exists(self.constants.ES_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "ES Configuration")
			if option == "Create":
				self.create_es_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "ES Configuration")
			self.modify_es_configuration() if option == "Modify" else self.display_es_configuration()


	def create_es_configuration(self) -> None:
		"""
		Method that creates the configuration for the connection between ElasticSearch and DI-Alert.
		"""
		es_data = libPyConfiguration(self.constants.BACKTITLE)
		es_data.define_es_host()
		es_data.define_verificate_certificate()
		es_data.define_use_authentication(self.constants.KEY_FILE)
		es_data.create_file(es_data.convert_object_to_dict(), self.constants.ES_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_es_configuration(self) -> None:
		"""
		Method that updates the configuration for the connection between ElasticSearch and DI-Alert.
		"""
		es_data = libPyConfiguration(self.constants.BACKTITLE)
		es_data.modify_configuration(self.constants.ES_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_es_configuration(self) -> None:
		"""
		Method that displays the configuration for the connection between ElasticSearch and DI-Alert.
		"""
		es_data = libPyConfiguration(self.constants.BACKTITLE)
		es_data.display_configuration(self.constants.ES_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def define_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the DI-Alert's configuration.
		"""
		if not path.exists(self.constants.DI_ALERT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "DI-Alert Configuration")
			if option == "Create":
				self.create_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "DI-Alert Configuration")
			self.modify_configuration() if option == "Modify" else self.display_configuration()


	def create_configuration(self) -> None:
		"""
		Method that creates the DI-Alert's configuration.
		"""
		di_alert_data = Configuration()
		di_alert_data.define_index_pattern()
		di_alert_data.define_timestamp_field()
		di_alert_data.define_range_time()
		di_alert_data.define_execution_time()
		di_alert_data.define_telegram_bot_token()
		di_alert_data.define_telegram_chat_id()
		di_alert_data.create_file(di_alert_data.convert_object_to_dict())


	def modify_configuration(self) -> None:
		"""
		Method that updates the DI-Alert's configuration.
		"""
		di_alert_data = Configuration()
		di_alert_data.modify_configuration()


	def display_configuration(self) -> None:
		"""
		Method that displays the DI-Alert's configuration.
		"""
		di_alert_data = Configuration()
		di_alert_data.display_configuration()


	def define_agent_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the DI-Alert-Agent's configuration.
		"""
		if not path.exists(self.constants.DI_ALERT_AGENT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "DI-Alert-Agent Configuration")
			if option == "Create":
				self.create_agent_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "DI-Alert-Agent Configuration")
			self.modify_agent_configuration() if option == "Modify" else self.display_agent_configuration()


	def create_agent_configuration(self) -> None:
		"""
		Method that creates the DI-Alert-Agent's configuration.
		"""
		di_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		di_alert_agent_data.define_frequency_time()
		di_alert_agent_data.define_telegram_bot_token(self.constants.KEY_FILE)
		di_alert_agent_data.define_telegram_chat_id(self.constants.KEY_FILE)
		di_alert_agent_data.create_file(vs_monitor_agent_data.convert_object_to_dict(), self.constants.DI_ALERT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_agent_configuration(self) -> None:
		"""
		Method that updates the DI-Alert-Agent's configuration.
		"""
		di_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		di_alert_agent_data.modify_agent_configuration(self.constants.DI_ALERT_AGENT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_agent_configuration(self) -> None:
		"""
		Method that displays the DI-Alert-Agent's configuration.
		"""
		di_alert_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		di_alert_agent_data.display_agent_configuration(self.constants.DI_ALERT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_about(self) -> None:
		"""
		Method that displays the about of the application.
		"""
		try:
			text = "\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/DI-Alert\nDI-Alert v3.2 - September 2025" + "\n\nPython tool that audits and validates the integrity of\ndocuments ingested in an Elasticsearch index."
			self.dialog.create_scrollbox(text, 13, 60, "About")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error") 
