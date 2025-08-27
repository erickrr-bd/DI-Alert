"""
Class that manages the application's constants.
"""
from typing import List
from dataclasses import dataclass, field

@dataclass(frozen = True)
class Constants:
	"""
	Message displayed in the background.
	"""
	BACKTITLE: str = "DI-ALERT-TOOL v3.2 by Erick Rodriguez"

	"""
	Configuration file for the connection between ElasticSearch and DI-Alert.
	"""
	ES_CONFIGURATION: str = "/etc/DI-Alert-Suite/DI-Alert/configuration/es_conf.yaml"

	"""
	DI-Alert's configuration file.
	"""
	DI_ALERT_CONFIGURATION: str = "/etc/DI-Alert-Suite/DI-Alert/configuration/di_alert.yaml"

	"""
	DI-Alert-Agent's configuration file.
	"""
	DI_ALERT_AGENT_CONFIGURATION: str = "/etc/DI-Alert-Suite/DI-Alert-Agent/configuration/di_alert_agent.yaml"

	"""
	Encryption key path.
	"""
	KEY_FILE: str = "/etc/DI-Alert-Suite/DI-Alert/configuration/key"

	"""
	DI-Alert-Tool log file.
	"""
	LOG_FILE: str = "/var/log/DI-Alert/di-alert-tool-log"

	"""
	Owner user.
	"""
	USER: str = "di_alert"

	"""
	Owner group.
	"""
	GROUP: str = "di_alert"

	"""
	Options displayed in the "Main" menu.
	"""
	MAIN_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "ES Configuration"), ("2", "Configuration"), ("3", "Index Validator"), ("4", "Service"), ("5", "About"), ("6", "Exit")])

	"""
	Options displayed in the "Configuration" menu.
	"""
	CONFIGURATION_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "DI-Alert"), ("2", "DI-Alert-Agent")])

	"""
	Options that are displayed when the configuration file doesn't exist.
	"""
	CONFIGURATION_OPTIONS_FALSE: List = field(default_factory = lambda : [("Create", "Create the configuration file", 0)])

	"""
	Options that are displayed when the configuration file exists.
	"""
	CONFIGURATION_OPTIONS_TRUE: List = field(default_factory = lambda : [("Modify", "Modify the configuration file", 0), ("Display", "Display the configuration file", 0)])

	"""
	Unit time.
	"""
	UNIT_TIME: List = field(default_factory = lambda: [["minutes", "Time expressed in minutes", 1], ["hours", "Time expressed in hours", 0], ["days", "Time expressed in days", 0]])

	"""
	Configuration's fields.
	"""
	CONFIGURATION_FIELDS: List = field(default_factory = lambda : [("Index", "ElasticSearch's index pattern(s)", 0), ("Timestamp", "Timestamp's Field", 0), ("Range Time", "Search range time", 0), ("Execution Time", "Integrity validation time", 0), ("Bot Token", "Telegram Bot Token", 0), ("Chat ID", "Telegram channel identifier", 0)]) 

	"""
	Options displayed in the "Index Pattern" menu.
	"""
	INDEX_PATTERN_OPTIONS = [("1", "Add New Index Pattern(s)"), ("2", "Modify Index Pattern(s)"), ("3", "Remove Index Pattern(s)")]

	"""
	Options displayed in the "Service" menu.
	"""
	SERVICE_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Start Service"), ("2", "Restart Service"), ("3", "Stop Service"), ("4", "Service Status")])
