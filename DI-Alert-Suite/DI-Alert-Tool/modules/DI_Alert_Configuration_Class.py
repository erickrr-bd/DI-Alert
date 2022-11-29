from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the DI-Alert configuration.
"""
class DIAlertConfiguration:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel: Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def createConfiguration(self):
		"""
		Method that creates the DI-Alert configuration.
		"""
		di_alert_data = []
		try:
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			master_nodes_total = self.__dialog.createInputBoxToNumberDialog("Enter the number of master nodes in the ElasticSearch cluster:", 9, 50, "1")
			list_to_form_dialog = self.__utils.createListToDialogForm(int(master_nodes_total), "IP Address")
			ips_master_nodes_es = self.__dialog.createFormDialog("Enter the IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "ElasticSearch Hosts")
			di_alert_data.append(ips_master_nodes_es)
			es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, "9200")
			di_alert_data.append(es_port)
			use_ssl_tls = self.__dialog.createYesOrNoDialog("\nDo you require DI-Alert to communicate with ElasticSearch using the SSL/TLS protocol?", 8, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				di_alert_data.append(True)
				verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require DI-Alert to verificate the SSL certificate?", 8, 50, "Certificate Verification")
				if verificate_certificate_ssl == "ok":
					di_alert_data.append(True)
					path_certificate_file = self.__dialog.createFileDialog("/etc/DI-Alert-Suite/DI-Alert", 8, 50, "Select the CA certificate:", ".pem")
					di_alert_data.append(path_certificate_file)
				else:
					di_alert_data.append(False)
			else:
				di_alert_data.append(False)
			use_authentication_method = self.__dialog.createYesOrNoDialog("\nIs it required to use an authentication mechanism (HTTP authentication or API key) to connect to ElasticSearch?", 9, 50, "Authentication Method")
			if use_authentication_method == "ok":
				di_alert_data.append(True)
				option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 9, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				di_alert_data.append(option_authentication_method)
				if option_authentication_method == "HTTP Authentication":
					user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
					di_alert_data.append(user_http_authentication.decode("utf-8"))
					password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 9, 50, "password", True), passphrase)
					di_alert_data.append(password_http_authentication.decode("utf-8"))
				elif option_authentication_method == "API Key":
					api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					di_alert_data.append(api_key_id.decode("utf-8"))
					api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					di_alert_data.append(api_key.decode("utf-8"))
			else:
				di_alert_data.append(False)
			index_pattern_total = self.__dialog.createInputBoxToNumberDialog("Enter the total number of index patterns that will be monitored:", 9, 50, "1")
			list_to_form_dialog = self.__utils.createListToDialogForm(int(index_pattern_total), "Index Pattern")
			index_pattern_es = self.__dialog.createFormDialog("Enter the index patterns", list_to_form_dialog, 15, 50, "Index Pattern")
			di_alert_data.append(index_pattern_es)
			days_ago = self.__dialog.createInputBoxToNumberDialog("Enter the range of days from the current one in which the data will be validated:", 9, 50, "1")
			di_alert_data.append(days_ago)
			time_execution = self.__dialog.createTimeDialog("Select the time of execution:", 2, 50, -1, -1)
			di_alert_data.append(str(time_execution[0]) + ':' + str(time_execution[1]))
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			di_alert_data.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			di_alert_data.append(telegram_chat_id.decode("utf-8"))
			self.__createYamlFileConfiguration(di_alert_data)
			if path.exists(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE):
				self.__dialog.createMessageDialog("\nDI-Alert configuration file created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("DI-Alert configuration file created", 1, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nError to encrypt or decrypt the data. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (FileNotFoundError, IOError, OSError) as exception:
			self.__dialog.createMessageDialog("\nError when executing an action on a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def modifyConfiguration(self):
		"""
		Method that allows to modify one or more values in the DI-Alert configuration file.
		"""
		di_alert_data = []
		try:
			di_alert_data = self.__utils.readYamlFile(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			options_di_alert_update = self.__dialog.createCheckListDialog("Select one or more options:", 16, 75, self.__constants.OPTIONS_DI_ALERT_UPDATE, "Modify DI-Alert Configuration")
			if "Hosts" in options_di_alert_update:
				option_es_hosts_update = self.__dialog.createMenuDialog("Select a option", 10, 50, self.__constants.OPTIONS_ES_HOSTS_UPDATE, "ELasticSearch Hosts Menu")
				if option_es_hosts_update == "1":
					master_nodes_total = self.__dialog.createInputBoxToNumberDialog("Enter the number of master nodes in the ElasticSearch cluster:", 9, 50, "1")
					list_to_form_dialog = self.__utils.createListToDialogForm(int(master_nodes_total), "IP Address")
					ips_master_nodes_es = self.__dialog.createFormDialog("Enter the IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "Add ElasticSearch Hosts")
					di_alert_data["es_host"].extend(ips_master_nodes_es)
				elif option_es_hosts_update == "2":
					list_to_form_dialog = self.__utils.convertListToDialogForm(di_alert_data["es_host"], "IP Address")
					ips_master_nodes_es = self.__dialog.createFormDialog("Enter the IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "Modify ElasticSearch Hosts")
					di_alert_data["es_host"] = ips_master_nodes_es
				elif option_es_hosts_update == "3":
					list_to_dialog = self.__utils.convertListToDialogList(di_alert_data["es_host"], "IP Address")
					options_remove_es_hosts = self.__dialog.createCheckListDialog("Select one or more options", 16, 50, list_to_dialog, "Remove ElasticSearch Hosts")
					self.__dialog.createScrollBoxDialog("\nThe following ElasticSearch Hosts were selected:\n\n" + '\n'.join(options_remove_es_hosts), 16, 55, "Remove ElasticSearch Hosts")
					confirm_remove_es_hosts = self.__dialog.createYesOrNoDialog("\nAre you sure to remove the ElasticSearch Hosts?", 8, 50, "Remove Confirmation")
					if confirm_remove_es_hosts == "ok":
						for option in options_remove_es_hosts:
							di_alert_data["es_host"].remove(option)
			if "Port" in options_di_alert_update:
				es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, str(di_alert_data["es_port"]))
				di_alert_data["es_port"] = int(es_port)
			if "SSL/TLS" in options_di_alert_update:
				if di_alert_data["use_ssl_tls"] == True:
					option_ssl_tls_true = self.__dialog.createRadioListDialog("Select a option:", 9, 70, self.__constants.OPTIONS_SSL_TLS_TRUE, "SSL/TLS Connection")
					if option_ssl_tls_true == "Disable":
						del di_alert_data["verificate_certificate_ssl"]
						if "path_certificate_file" in di_alert_data:
							del di_alert_data["path_certificate_file"]
						di_alert_data["use_ssl_tls"] = False
					elif option_ssl_tls_true == "Certificate Verification":
						if di_alert_data["verificate_certificate_ssl"] == True:
							option_verification_certificate_true = self.__dialog.createRadioListDialog("Select a option:", 9, 70, self.__constants.OPTIONS_VERIFICATION_CERTIFICATE_TRUE, "Certificate Verification")
							if option_verification_certificate_true == "Disable":
								if "path_certificate_file" in di_alert_data:
									del di_alert_data["path_certificate_file"]
								di_alert_data["verificate_certificate_ssl"] = False
							elif option_verification_certificate_true == "Certificate File":
								path_certificate_file = self.__dialog.createFileDialog(di_alert_data["path_certificate_file"], 8, 50, "Select the CA certificate:", ".pem")
								di_alert_data["path_certificate_file"] = path_certificate_file
						else:
							option_verification_certificate_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_VERIFICATION_CERTIFICATE_FALSE, "Certificate Verification")
							if option_verification_certificate_false == "Enable":
								di_alert_data["verificate_certificate_ssl"] = True
								path_certificate_file = self.__dialog.createFileDialog("/etc/DI-Alert-Suite/DI-Alert", 8, 50, "Select the CA certificate:", ".pem")
								verificate_certificate_ssl_json = {"path_certificate_file" : path_certificate_file}
								di_alert_data.update(verificate_certificate_ssl_json)
				else:
					option_ssl_tls_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_SSL_TLS_FALSE, "SSL/TLS Connection")
					di_alert_data["use_ssl_tls"] = True
					verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require DI-Alert to validate the SSL certificate?", 8, 50, "Certificate Verification")
					if verificate_certificate_ssl == "ok":
						path_certificate_file = self.__dialog.createFileDialog("/etc/DI-Alert-Suite/DI-Alert", 8, 50, "Select the CA certificate:", ".pem")
						verificate_certificate_ssl_json = {"verificate_certificate_ssl" : True, "path_certificate_file" : path_certificate_file}
					else:
						verificate_certificate_ssl_json = {"verificate_certificate_ssl" : False}
					di_alert_data.update(verificate_certificate_ssl_json)
			if "Authentication" in options_di_alert_update:
				if di_alert_data["use_authentication_method"] == True:
					option_authentication_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_AUTHENTICATION_TRUE, "Authentication Method")
					if option_authentication_true == "Data":
						if di_alert_data["authentication_method"] == "HTTP Authentication":
							option_authentication_method_true = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_AUTHENTICATION_METHOD_TRUE, "HTTP Authentication")
							if option_authentication_method_true == "Data":
								options_http_authentication_data = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_HTTP_AUTHENTICATION_DATA, "HTTP Authentication")	
								if "Username" in options_http_authentication_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)									
									di_alert_data["user_http_authentication"] = user_http_authentication.decode("utf-8")
								elif "Password" in options_http_authentication_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
									di_alert_data["password_http_authentication"] = password_http_authentication.decode("utf-8")
							elif option_authentication_method_true == "Disable":
								passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
								api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
								api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
								del di_alert_data["user_http_authentication"]
								del di_alert_data["password_http_authentication"]
								di_alert_data["authentication_method"] = "API Key"
								api_key_json = {"api_key_id" : api_key_id.decode("utf-8"), "api_key" : api_key.decode("utf-8")}
								di_alert_data.update(api_key_json)
						elif di_alert_data["authentication_method"] == "API Key":
							option_authentication_method_true = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_AUTHENTICATION_METHOD_TRUE, "API Key")
							if option_authentication_method_true == "Data":
								options_api_key_data = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_API_KEY_DATA, "API Key")
								if "API Key ID" in options_api_key_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
									di_alert_data["api_key_id"] = api_key_id.decode("utf-8")
								elif "API Key" in options_api_key_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
									di_alert_data["api_key"] = api_key.decode("utf-8")
							elif option_authentication_method_true == "Disable":
								passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
								user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
								password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
								del di_alert_data["api_key_id"]
								del di_alert_data["api_key"]
								di_alert_data["authentication_method"] = "HTTP Authentication"
								http_authentication_json = {"user_http_authentication" : user_http_authentication.decode("utf-8"), "password_http_authentication" : password_http_authentication.decode("utf-8")}
								di_alert_data.update(http_authentication_json)
					elif option_authentication_true == "Disable":
						di_alert_data["use_authentication_method"] = False
						if di_alert_data["authentication_method"] == "HTTP Authentication":
							del di_alert_data["user_http_authentication"]
							del di_alert_data["password_http_authentication"]
						elif di_alert_data["authentication_method"] == "API Key":
							del di_alert_data["api_key_id"]
							del di_alert_data["api_key"]
						del di_alert_data["authentication_method"]
				else:
					option_authentication_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_AUTHENTICATION_FALSE, "Authentication Method")
					if option_authentication_false == "Enable":
						di_alert_data["use_authentication_method"] = True
						option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 10, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
						if option_authentication_method == "HTTP authentication":
							passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
							user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
							password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
							http_authentication_json = {"authentication_method" : "HTTP authentication", "user_http_authentication" : user_http_authentication.decode("utf-8"), "password_http_authentication" : password_http_authentication.decode("utf-8")}
							di_alert_data.update(http_authentication_json)
						elif option_authentication_method == "API Key":
							passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
							api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
							api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
							api_key_json = {"authentication_method" : "API Key", "api_key_id" : api_key_id.decode("utf-8"), "api_key" : api_key.decode("utf-8")}
							di_alert_data.update(api_key_json)
			if "Index Patterns" in options_di_alert_update:
				option_index_patterns_update = self.__dialog.createMenuDialog("Select a option:", 10, 50, self.__constants.OPTIONS_INDEX_PATTERNS_UPDATE, "Index Patterns Menu")
				if option_index_patterns_update == "1":
					index_pattern_total = self.__dialog.createInputBoxToNumberDialog("Enter the total number of index patterns that will be monitored:", 9, 50, "1")
					list_to_form_dialog = self.__utils.createListToDialogForm(int(index_pattern_total), "Index Pattern")
					index_pattern_es = self.__dialog.createFormDialog("Enter the index patterns:", list_to_form_dialog, 15, 50, "Add Index Pattern")
					di_alert_data["index_pattern_es"].extend(index_pattern_es)
				elif option_index_patterns_update == "2":
					list_to_form_dialog = self.__utils.convertListToDialogForm(di_alert_data["index_pattern_es"], "Index Pattern")
					index_pattern_es = self.__dialog.createFormDialog("Enter the index patterns:", list_to_form_dialog, 15, 50, "Modify Index Pattern")
					di_alert_data["index_pattern_es"] = index_pattern_es
				elif option_index_patterns_update == "3":
					list_to_dialog = self.__utils.convertListToDialogList(di_alert_data["index_pattern_es"], "Index Pattern")
					options_remove_index_patterns = self.__dialog.createCheckListDialog("Select one or more options", 16, 50, list_to_dialog, "Remove Index Pattern")
					self.__dialog.createScrollBoxDialog("\nThe following Index Patterns were selected:\n\n" + '\n'.join(options_remove_index_patterns), 16, 55, "Remove Index Pattern")
					confirm_remove_index_patterns = self.__dialog.createYesOrNoDialog("\nAre you sure to remove the Index Patterns?", 8, 50, "Remove Confirmation")
					if confirm_remove_index_patterns == "ok":
						for option in options_remove_index_patterns:
							di_alert_data["index_pattern_es"].remove(option)
			if "Days Ago" in options_di_alert_update:
				days_ago = self.__dialog.createInputBoxToNumberDialog("Enter the range of days from the current one in which the data will be validated:", 9, 50, str(di_alert_data["days_ago"]))
				di_alert_data["days_ago"] = int(days_ago)
			if "Time Execution" in options_di_alert_update:
				time_execution_actual = di_alert_data["time_execution"].split(':')
				time_execution = self.__dialog.createTimeDialog("Select the time of execution:", 2, 50, int(time_execution_actual[0]), int(time_execution_actual[1]))
				di_alert_data["time_execution"] = str(time_execution[0]) + ':' + str(time_execution[1])
			if "Bot Token" in options_di_alert_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.__utils.decryptDataWithAES(di_alert_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
				di_alert_data["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
			if "Chat ID" in options_di_alert_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.__utils.decryptDataWithAES(di_alert_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
				di_alert_data["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
			self.__utils.createYamlFile(di_alert_data, self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			if hash_file_configuration_new == hash_file_configuration_original:
				self.__dialog.createMessageDialog("\nDI-Alert Configuration not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nDI-Alert Configuration modified.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("DI-Alert Configuration modified", 2, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except KeyError as exception:
			self.__dialog.createMessageDialog("\nKey Error: " + str(exception), 7, 50, "Error Message")
			self.__logger.generateApplicationLog("Key Error: " + str(exception), 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nError to encrypt or decrypt the data. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		except (IOError, OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError when executing an action on a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def showConfigurationData(self):
		"""
		Method that displays the data stored in the DI-Alert configuration file.
		"""
		try:
			di_alert_data = self.__utils.convertDataYamlFileToString(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
			message_to_display = "\nDI-Alert Configuration:\n\n" + di_alert_data
			self.__dialog.createScrollBoxDialog(message_to_display, 18, 70, "DI-Alert Configuration")
		except (IOError, OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nError when executing an action on a file or folder. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		finally:
			self.__action_to_cancel()


	def __createYamlFileConfiguration(self, di_alert_data):
		"""
		Method that creates the YAML File that corresponds to the DI-Alert configuration.

		:arg di_alert_data (dict): Object that contains the data that will save in the configuration file. 
		"""
		di_alert_data_json = {
			"es_host" : di_alert_data[0],
			"es_port" : int(di_alert_data[1]),
			"use_ssl_tls" : di_alert_data[2]
		}

		if di_alert_data[2] == True:
			if di_alert_data[3] == True:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : di_alert_data[3], "path_certificate_file" : di_alert_data[4]}
				last_index = 4
			else:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : di_alert_data[3]}
				last_index = 3
			di_alert_data_json.update(verificate_certificate_ssl_json)
		else:
			last_index = 2
		if di_alert_data[last_index + 1] == True:
			if di_alert_data[last_index + 2] == "HTTP Authentication":
				http_authentication_json = {"use_authentication_method" : di_alert_data[last_index + 1], "authentication_method" : di_alert_data[last_index + 2], "user_http_authentication" : di_alert_data[last_index + 3], "password_http_authentication" : di_alert_data[last_index + 4]}
				di_alert_data_json.update(http_authentication_json)
			elif di_alert_data[last_index + 2] == "API Key":
				api_key_json = {"use_authentication_method" : di_alert_data[last_index + 1], "authentication_method" : di_alert_data[last_index + 2], "api_key_id" : di_alert_data[last_index + 3], "api_key" : di_alert_data[last_index + 4]}
				di_alert_data_json.update(api_key_json)
			last_index += 4
		else:
			authentication_method_json = {"use_authentication_method" : di_alert_data[last_index + 1]}
			di_alert_data_json.update(authentication_method_json)
			last_index += 1
		di_alert_data_aux_json = {"index_pattern_es" : di_alert_data[last_index + 1], "days_ago" : int(di_alert_data[last_index + 2]), "time_execution" : di_alert_data[last_index + 3], "telegram_bot_token" : di_alert_data[last_index + 4], "telegram_chat_id" : di_alert_data[last_index + 5]}
		di_alert_data_json.update(di_alert_data_aux_json)

		self.__utils.createYamlFile(di_alert_data_json, self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE)
		self.__utils.changeOwnerToPath(self.__constants.PATH_DI_ALERT_CONFIGURATION_FILE, self.__constants.USER, self.__constants.GROUP)