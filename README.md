# DI-Alert v3.2 (Data Integrity - Alert)

Python tool that audits and validates the documents' integrity ingested in an Elasticsearch index.

Allows to validate that documents within an index haven't been modified unexpectedly, ensuring consistency and traceability in business environments.

Ideal tool for compliance and alignment with frameworks such as ISO 27001, NIST SP 800-53, and PCI DSS.

## Features
- Integrity verification by documents' version field (`_version`)
- Scheduled audit using APScheduler
- Modular and extensible for multiple indices or index patterns
- It runs each day at a specific configurable time
- Audits index pattern documents in a configurable time range
- Audit of a specific index
- Supports running as a service/daemon on Linux and Windows
- Alert via Telegram

## Requirements
- Red Hat 8 o Rocky Linux 8
- ElasticSearch 7.x or 8.x
- Python 3.12+
- Python libraries
  - libPyElk v2.2 [(https://github.com/erickrr-bd/libPyElk)](https://github.com/erickrr-bd/libPyElk)
  - libPyDialog v2.2 [(https://github.com/erickrr-bd/libPyDialog)](https://github.com/erickrr-bd/libPyDialog)
  - libPyConfiguration v1.0 [(https://github.com/erickrr-bd/libPyConfiguration)](https://github.com/erickrr-bd/libPyConfiguration)
  - libPyAgentConfiguration v1.0 [(https://github.com/erickrr-bd/libPyAgentConfiguration)](https://github.com/erickrr-bd/libPyAgentConfiguration)
  - libPyTelegram v1.2 [(https://github.com/erickrr-bd/libPyTelegram)](https://github.com/erickrr-bd/libPyTelegram)
  - libPyUtils v2.2 [(https://github.com/erickrr-bd/libPyUtils)](https://github.com/erickrr-bd/libPyUtils)
  - libPyLog v2.2 [(https://github.com/erickrr-bd/libPyLog)](https://github.com/erickrr-bd/libPyLog)
  - APScheduler

## Tools

### DI-Alert

Automated solution that audits document integrity across multiple index patterns within Elasticsearch. Executes validations in configurable time ranges, verifying that documents haven't been modified outside of authorized flows.

The tool operates at defined times, allowing its integration with audit schedules or maintenance windows. Upon detection of altered, duplicate or inconsistent version documents, it issues immediate alerts via Telegram, facilitating a timely response by the security team.

Designed for regulated environments, this solution contributes to compliance with standards such as ISO 27001, NIST SP 800-92 and PCI DSS, reinforcing traceability, data governance and early incident detection.

### DI-Alert-Agent

Tool designed to continuously monitor the operational status of the DI-Alert daemon, responsible for critical notification tasks. Performs periodic verifications of availability and health of the service, detecting interruptions or failures in its execution.

When the daemon isn't active, the system generates an immediate alert via Telegram, notifying the responsible team. Additionally, it executes an automatic recovery procedure, trying to restart the service in a controlled manner, in accordance with operational continuity policies.

### DI-Alert-Tool

Application designed to centrally manage the configuration and operational status of the DI-Alert daemon, through an intuitive and easy-to-use graphical interface. It allows you to view, edit and validate key service parameters, as well as start, stop or restart the daemon in a controlled manner.

The tool facilitates operational management in technical environments, reducing dependence on manual commands and improving change traceability. 
 
## Installation 

The tool has its own installer, to facilitate the installation process. First, it's necessary to assign execution permissions to the di_alert_installer.sh file:

`chmod +x di_alert_installer.sh`

The binary is then executed as follows:

`./di_alert_installer.sh`

**NOTE:** The installer has two options. Option 'I' installs the application for the first time, ideal when you don't have a previous version. The 'U' option updates the version while maintaining some configuration files.

## Contributions

Contributions are welcome! You can open an issue or send a pull request with improvements, new validations or integrations.
