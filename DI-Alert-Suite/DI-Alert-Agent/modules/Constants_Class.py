"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Absolute path of the DI-Alert-Agent configuration file.
	"""
	PATH_DI_ALERT_AGENT_CONFIGURATION_FILE = "/etc/DI-Alert-Suite/DI-Alert-Agent/configuration/di_alert_agent_conf.yaml"

	"""
	Absolute path of the file where the key for the encryption/decryption process is stored.
	"""
	PATH_KEY_FILE = "/etc/DI-Alert-Suite/DI-Alert/configuration/key"

	"""
	Absolute path of the application logs.
	"""
	NAME_FILE_LOG = "/var/log/DI-Alert/di-alert-agent-log-"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "di_alert"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "di_alert"