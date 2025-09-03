"""
Class that manages the application's constants.
"""
from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
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
	LOG_FILE: str = "/var/log/DI-Alert/di-alert-agent-log"

	"""
	Owner user.
	"""
	USER: str = "di_alert"

	"""
	Owner group.
	"""
	GROUP: str = "di_alert"
