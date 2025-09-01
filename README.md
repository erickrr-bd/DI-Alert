# DI-Alert v3.2 (Data Integrity - Alert)

Python tool that audits and validates the documents' integrity ingested in an Elasticsearch index.

Allows to validate that documents within an index haven't been modified unexpectedly, ensuring consistency and traceability in business environments.

## Features
- Integrity verification by version (`_version`) of documents
- Scheduled audit using cron or APScheduler
- Supports running as a service/daemon on Linux and Windows
- Modular and extensible for multiple indices or index patterns
- Alert via Telegram

## Requirements
- Red Hat 8 o Rocky Linux 8
- ElasticSearch 7.x or 8.x
- Python 3.12+
- Python libraries
  - libPyElk
  - libPyTelegram
  - libPyUtils
  - libPyLog
  - APScheduler
 
## Installation 

## Contributions

Contributions are welcome! You can open an issue or send a pull request with improvements, new validations or integrations.
