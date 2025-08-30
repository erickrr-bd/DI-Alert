"""
Class that manages everything related to the DI-Alert's configuration.
"""
from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from dataclasses import dataclass, field

@dataclass
class Configuration:

	index_pattern: dict = field(default_factory = dict)
	timestamp_field: str = None
	range_time: dict = field(default_factory = dict)
	execution_time: str = None
	telegram_bot_token: tuple = field(default_factory = tuple)
	telegram_chat_id: tuple = field(default_factory = tuple)


	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def define_index_pattern(self) -> None:
		"""
		Method that defines the Index Pattern(s).
		"""
		total_index_pattern = self.dialog.create_integer_inputbox("Enter the total number of Index Pattern:", 8, 50, "1")
		tuple_to_form = self.utils.generate_tuple_to_form(int(total_index_pattern), "Index Pattern")
		self.index_pattern = self.dialog.create_form("Enter Index Pattern(s):", tuple_to_form, 15, 55, "Index Pattern(s)", True, validation_type = 3)


	def define_timestamp_field(self) -> None:
		"""
		Method that defines the field's name corresponding to the index timestamp.
		"""
		self.timestamp_field = self.dialog.create_inputbox("Enter the field's name that corresponds to the index timestamp:", 9, 50, "@timestamp")


	def define_range_time(self) -> None:
		"""
		Method that defines the time range from the current moment in which the event search will be performed.
		"""
		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.UNIT_TIME, "Unit Time")
		size = 9 if option == "minutes" else 8
		total_time = self.dialog.create_integer_inputbox(f"Enter the total in {option} of the search range:", size, 50, "1")
		self.range_time = {option : int(total_time)}


	def define_execution_time(self) -> None:
		"""
		Method that defines the time at which the index pattern validation will be executed.
		"""
		selected_time = self.dialog.create_time("Select the time:", 2, 50, -1, -1)
		self.execution_time = f"{selected_time[0]}:{selected_time[1]}"


	def define_telegram_bot_token(self) -> None:
		"""
		Method that defines the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)


	def define_telegram_chat_id(self) -> None:
		"""
		Method that defines the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, "-1002365478941"), passphrase)


	def modify_index_pattern(self) -> None:
		"""
		Method that modifies Index Pattern(s).
		"""
		option = self.dialog.create_menu("Select a option:", 10, 50, self.constants.INDEX_PATTERN_OPTIONS, "Index Pattern Menu")
		match option:
			case "1":		
				total_index_pattern = self.dialog.create_integer_inputbox("Enter the total number of Index Pattern:", 8, 50, "1")
				tuple_to_form = self.utils.generate_tuple_to_form(int(total_index_pattern), "Index Pattern")
				index_pattern = self.dialog.create_form("Enter Index Pattern(s):", tuple_to_form, 15, 55, "Add Index Pattern(s)", True, validation_type = 3)
				self.index_pattern.extend(index_pattern)
				self.logger.create_log(f"Added Index Pattern(s): {','.join(index_pattern)}", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case "2":
				tuple_to_form = self.utils.convert_list_to_tuple(self.index_pattern, "Index Pattern")
				self.index_pattern = self.dialog.create_form("Enter Index Pattern(s):", tuple_to_form, 15, 50, "Modify Index Pattern(s)", True, validation_type = 3)
				self.logger.create_log(f"Modified Index Pattern(s): {','.join(self.index_pattern)}", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case "3":
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(self.index_pattern, "Index Pattern")
				options = self.dialog.create_checklist("Select one or more options:", 15, 50, tuple_to_rc, "Remove Index Pattern(s)")
				text = self.utils.get_str_from_list(options, "Selected Index Pattern(s):")
				self.dialog.create_scrollbox(text, 15, 60, "Remove Index Pattern(s)")
				index_pattern_yn = self.dialog.create_yes_or_no("\nAre you sure to remove the selected Index Pattern(s)?\n\n** This action cannot be undone.", 10, 50, "Remove Index Pattern(s)")
				if index_pattern_yn == "ok":
					[self.index_pattern.remove(option) for option in options]
				self.logger.create_log(f"Removed Index Pattern(s): {','.join(options)}", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_timestamp_field(self) -> None:
		"""
		Method that modifies the field's name corresponding to the index timestamp.
		"""
		self.timestamp_field = self.dialog.create_inputbox("Enter the field's name that corresponds to the index timestamp:", 9, 50, self.timestamp_field)
		self.logger.create_log(f"Timestamp's field modified: {self.timestamp_field}", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_range_time(self) -> None:
		"""
		Method that modifies the search time range.
		"""
		old_unit_time = list(self.range_time.keys())[0]

		for unit in self.constants.UNIT_TIME:
			if unit[0] == old_unit_time:
				unit[2] = 1
			else:
				unit[2] = 0

		option = self.dialog.create_radiolist("Select a option:", 10, 50, self.constants.UNIT_TIME, "Unit Time")
		size = 9 if option == "minutes" else 8
		total_time = self.dialog.create_integer_inputbox(f"Enter the total in {option} of the search range:", size, 50, str(self.range_time[old_unit_time]))
		self.range_time = {option : int(total_time)}
		self.logger.create_log(f"Range time modified: {self.range_time}", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_execution_time(self) -> None:
		"""
		Method that modifies the time at which the index pattern validation will be executed.
		"""
		old_execution_time = self.execution_time.split(':')
		selected_time = self.dialog.create_time("Select the time:", 2, 50, int(old_execution_time[0]), int(old_execution_time[1]))
		self.execution_time = f"{selected_time[0]}:{selected_time[1]}"
		self.logger.create_log(f"Execution Time modified: {self.execution_time}", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_telegram_bot_token(self) -> None:
		"""
		Method that modifies the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, self.utils.decrypt_data(self.telegram_bot_token, passphrase).decode("utf-8")), passphrase)
		self.logger.create_log("Telegram Bot Token modified.", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def modify_telegram_chat_id(self) -> None:
		"""
		Method that modifies the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, self.utils.decrypt_data(self.telegram_chat_id, passphrase).decode("utf-8")), passphrase)
		self.logger.create_log("Telegram Chat ID modified.", 3, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def convert_object_to_dict(self) -> dict:
		"""
		Method that converts a Configuration's object into a dictionary.

		Returns:
			configuration_data_json (dict): Dictionary with the object's data.
		"""
		configuration_data_json = {
			"index_pattern" : self.index_pattern,
			"timestamp_field" : self.timestamp_field,
			"range_time" : self.range_time,
			"execution_time" : self.execution_time,
			"telegram_bot_token" : self.telegram_bot_token,
			"telegram_chat_id" : self.telegram_chat_id
		}
		return configuration_data_json


	def convert_dict_to_object(self, configuration_data: dict) -> None:
		"""
		Method that converts a dictionary into an Configuration's object.

		Parameters:
			configuration_data (dict): Dictionary to convert.
		"""
		self.index_pattern = configuration_data["index_pattern"]
		self.timestamp_field = configuration_data["timestamp_field"]
		self.range_time = configuration_data["range_time"]
		self.execution_time = configuration_data["execution_time"]
		self.telegram_bot_token = configuration_data["telegram_bot_token"]
		self.telegram_chat_id = configuration_data["telegram_chat_id"]


	def create_file(self, configuration_data: dict) -> None:
		"""
		Method that creates the YAML file corresponding to the configuration.

		Parameters:
			configuration_data (dict): Data to save in the YAML file.
		"""
		try:
			self.utils.create_yaml_file(configuration_data, self.constants.DI_ALERT_CONFIGURATION)
			self.utils.change_owner(self.constants.DI_ALERT_CONFIGURATION, self.constants.USER, self.constants.GROUP, "640")
			if path.exists(self.constants.DI_ALERT_CONFIGURATION):
				self.dialog.create_message("\nConfiguration created.", 7, 50, "Notification Message")
				self.logger.create_log("Configuration created", 2, "__createDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.create_message("\nError creating configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def modify_configuration(self) -> None:
		"""
		Method that modifies the configuration.
		"""
		try:
			options = self.dialog.create_checklist("Select one or more options:", 13, 75, self.constants.CONFIGURATION_FIELDS, "Configuration Fields")
			configuration_data = self.utils.read_yaml_file(self.constants.DI_ALERT_CONFIGURATION)
			self.convert_dict_to_object(configuration_data)
			original_hash = self.utils.get_hash_from_file(self.constants.DI_ALERT_CONFIGURATION)
			if "Index" in options:
				self.modify_index_pattern()
			if "Timestamp" in options:
				self.modify_timestamp_field()
			if "Range Time" in options:
				self.modify_range_time()
			if "Execution Time" in options:
				self.modify_execution_time()
			if "Bot Token" in options:
				self.modify_telegram_bot_token()
			if "Chat ID" in options:
				self.modify_telegram_chat_id()
			configuration_data = self.convert_object_to_dict()
			self.utils.create_yaml_file(configuration_data, self.constants.DI_ALERT_CONFIGURATION)
			new_hash = self.utils.get_hash_from_file(self.constants.DI_ALERT_CONFIGURATION)
			if new_hash == original_hash:
				self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
			else:
				self.dialog.create_message("\nConfiguration modified.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError modifying configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_modifyDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_configuration(self) -> None:
		"""
		Method that displays the configuration file's data.
		"""
		try:
			configuration_data = self.utils.convert_yaml_to_str(self.constants.DI_ALERT_CONFIGURATION)
			text = "\nData:\n\n" + configuration_data
			self.dialog.create_scrollbox(text, 18, 70, "Configuration")
		except Exception as exception:
			self.dialog.create_message("\nError displaying configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_displayDAConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")
