"""
Class that manages the application's constants.
"""
from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
	"""
	Configuration file for the connection between ElasticSearch and DI-Alert.
	"""
	ES_CONFIGURATION: str = "/etc/DI-Alert-Suite/DI-Alert/configuration/es_conf.yaml"

	"""
	DI-Alert's configuration file.
	"""
	DI_ALERT_CONFIGURATION: str = "/etc/DI-Alert-Suite/DI-Alert/configuration/di_alert.yaml"

	"""
	Encryption key path.
	"""
	KEY_FILE: str = "/etc/DI-Alert-Suite/DI-Alert/configuration/key"

	"""
	DI-Alert-Tool log file.
	"""
	LOG_FILE: str = "/var/log/DI-Alert/di-alert-log"

	"""
	Owner user.
	"""
	USER: str = "di_alert"

	"""
	Owner group.
	"""
	GROUP: str = "di_alert"
