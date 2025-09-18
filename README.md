# DI-Alert v3.2 (Data Integrity - Alert)

Python tool that audits and validates the documents' integrity ingested in an Elasticsearch index.

Allows to validate that documents within an index haven't been modified unexpectedly, ensuring consistency and traceability in business environments.

Ideal tool for compliance and alignment with frameworks such as ISO 27001, NIST SP 800-53, and PCI DSS.

## Features
- Integrity verification by documents' version field (`_version`)
- Scheduled audit using cron or APScheduler
- Supports running as a service/daemon on Linux and Windows
- Modular and extensible for multiple indices or index patterns
- Audit of a specific index
- Alert via Telegram

## Requirements
- Red Hat 8 o Rocky Linux 8
- ElasticSearch 7.x or 8.x
- Python 3.12+
- Python libraries
  - [libPyElk v2.2](https://github.com/erickrr-bd/libPyElk)
  - [libPyDialog v2.2](https://github.com/erickrr-bd/libPyDialog)
  - [libPyConfiguration v1.0](https://github.com/erickrr-bd/libPyConfiguration)
  - [libPyAgentConfiguration v1.0](https://github.com/erickrr-bd/libPyAgentConfiguration)
  - [libPyTelegram v1.2](https://github.com/erickrr-bd/libPyTelegram)
  - [libPyUtils v2.2](https://github.com/erickrr-bd/libPyUtils)
  - [libPyLog v2.2](https://github.com/erickrr-bd/libPyLog)
  - APScheduler
 
## Installation 

The tool has its own installer, to facilitate the installation process. First, it is necessary to assign execution permissions to the di_alert_installer.sh file:

`chmod +x di_alert_installer.sh`

The binary is then executed as follows:

`./di_alert_installer.sh`

**NOTE: ** The installer has two options. Option 'I' installs the application for the first time, ideal when you don't have a previous version. The 'U' option updates the version while maintaining some configuration files.

## Contributions

Contributions are welcome! You can open an issue or send a pull request with improvements, new validations or integrations.
