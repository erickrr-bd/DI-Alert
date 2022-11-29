"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Title that is shown in the background of the application.
	"""
	BACKTITLE = "DI-ALERT-TOOL v3.1 by Erick Rodriguez"

	"""
	Absolute path of the DI-Alert configuration file.
	"""
	PATH_DI_ALERT_CONFIGURATION_FILE = "/etc/DI-Alert-Suite/DI-Alert/configuration/di_alert_conf.yaml"

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
	NAME_FILE_LOG = "/var/log/DI-Alert/di-alert-tool-log-"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "di_alert"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "di_alert"

	"""
	Options displayed in the "Main" menu.
	"""
	OPTIONS_MAIN_MENU = [("1", "DI-Alert Configuration"),
				  	  	 ("2", "DI-Alert Service"),
				  	  	 ("3", "DI-Alert-Agent"),
				  	  	 ("4", "Index Validator"),
				  	  	 ("5", "About"),
			      	  	 ("6", "Exit")]

	"""
	Options that are shown when the configuration file does not exist.
	"""
	OPTIONS_CONFIGURATION_FALSE = [("Create", "Create the configuration file", 0)]

	"""
	Options that are shown when the configuration file exists.
	"""
	OPTIONS_CONFIGURATION_TRUE = [("Modify", "Modify the configuration file", 0),
								  ("Show", "Show the configuration data", 0)]

	"""
	Options that are displayed to select an unit time.
	"""
	OPTIONS_UNIT_TIME = [["minutes", "Time expressed in minutes", 1],
					  	 ["hours", "Time expressed in hours", 0],
					  	 ["days", "Time expressed in days", 0]]

	"""
	Options that are displayed to select an authentication method.
	"""
	OPTIONS_AUTHENTICATION_METHOD = [("HTTP Authentication", "Use HTTP Authentication", 0),
								     ("API Key", "Use API Key", 0)]

	"""
	Options that are shown when a value is going to be modified in the DI-Alert configuration.
	"""
	OPTIONS_DI_ALERT_UPDATE = [("Hosts", "ElasticSearch Hosts", 0),
							   ("Port", "ElasticSearch Port", 0),
							   ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							   ("Authentication", "Enable or disable authentication method", 0),
							   ("Index Patterns", "Index patterns to validate", 0), 
							   ("Days Ago", "Time range in which index data will be validated", 0),
							   ("Time Execution", "Time in which the index data will be validated", 0),
							   ("Bot Token", "Telegram Bot Token", 0),
							   ("Chat ID", "Telegram channel identifier", 0)]

	"""
	Options that are displayed when "ElasticSearch hosts" option is modify.
	"""
	OPTIONS_ES_HOSTS_UPDATE = [("1", "Add New Hosts"),
							   ("2", "Modify Hosts"),
							   ("3", "Remove Hosts")]

	"""
	Options displayed when the use of SSL/TLS is enabled.
	"""
	OPTIONS_SSL_TLS_TRUE = [("Disable", "Disable SSL/TLS communication", 0),
							("Certificate Verification", "Modify certificate verification", 0)]

	"""
	Options displayed when the use of SSL/TLS is disabled.
	"""
	OPTIONS_SSL_TLS_FALSE = [("Enable", "Enable SSL/TLS communication", 0)]

	"""
	Options displayed when SSL certificate verification is enabled.
	"""
	OPTIONS_VERIFICATION_CERTIFICATE_TRUE = [("Disable", "Disable certificate verification", 0),
								   		     ("Certificate File", "Change certificate file", 0)]

	"""
	Options displayed when SSL certificate verification is disabled.
	"""
	OPTIONS_VERIFICATION_CERTIFICATE_FALSE = [("Enable", "Enable certificate verification", 0)]

	"""
	Options that are displayed when authentication is enabled.
	"""
	OPTIONS_AUTHENTICATION_TRUE = [("Data", "Modify authentication method", 0),
								   ("Disable", "Disable authentication method", 0)]

	"""
	Options that are displayed when modify an authentication method.
	"""
	OPTIONS_AUTHENTICATION_METHOD_TRUE = [("Data", "Modify authentication method data", 0),
								   	      ("Disable", "Disable authentication method", 0)]

	"""
	Options that are displayed when authentication is disabled.
	"""
	OPTIONS_AUTHENTICATION_FALSE = [("Enable", "Enable authentication", 0)]

	"""
	Options that are displayed when the HTTP authentication credentials are to be modified.
	"""
	OPTIONS_HTTP_AUTHENTICATION_DATA = [("Username", "Username for HTTP Authentication", 0),
								 		("Password", "User password", 0)]

	"""
	Options that are displayed when the API Key credentials are to be modified.
	"""
	OPTIONS_API_KEY_DATA = [("API Key ID", "API Key Identifier", 0),
							("Api Key", "API Key", 0)]

	"""
	Options that are displayed when "Index Patterns" option is modify.
	"""
	OPTIONS_INDEX_PATTERNS_UPDATE = [("1", "Add New Index Patterns"),
							         ("2", "Modify Index Patterns"),
							         ("3", "Remove Index Patterns")]

	"""
	Options displayed in the "Service" menu.
	"""
	OPTIONS_SERVICE_MENU = [("1", "Start Service"),
				            ("2", "Restart Service"),
				            ("3", "Stop Service"),
				            ("4", "Service Status")]

	"""
	Options displayed in the "DI-Alert-Agent" menu.
	"""
	OPTIONS_DI_ALERT_AGENT_MENU = [("1", "Configuration"),
							   	   ("2", "DI-Alert-Agent Service")]

	"""
	Options that are shown when a value is going to be modified in the DI-Alert-Agent configuration.
	"""
	OPTIONS_DI_ALERT_AGENT_UPDATE = [("First Execution", "First time the service is validated", 0),
							 		 ("Second Execution", "Second time the service is validated", 0),
							 		 ("Bot Token", "Telegram Bot Token", 0),
							 		 ("Chat ID", "Telegram channel identifier", 0)]