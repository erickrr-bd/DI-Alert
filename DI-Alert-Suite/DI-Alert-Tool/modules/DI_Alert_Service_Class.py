from libPyLog import libPyLog
from io import open as open_io
from libPyUtils import libPyUtils
from os import system, path, remove
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the DI-Alert service.
"""
class DIAlertService:

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


	def startService(self):
		"""
		Method to start the DI-Alert service.
		"""
		result = system("systemctl start di-alert.service")
		if int(result) == 0:
			self.__dialog.createMessageDialog("\nDI-Alert service started.", 7, 50, "Notification Message")
			self.__logger.generateApplicationLog("DI-Alert service started", 1, "__service", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif int(result) == 1280:
			self.__dialog.createMessageDialog("\nFailed to start DI-Alert service. Not found.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog("Failed to start DI-Alert service. Not found.", 3, "__service", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		self.__action_to_cancel()


	def restartService(self):
		"""
		Method to restart the DI-Alert service.
		"""
		result = system("systemctl restart di-alert.service")
		if int(result) == 0:
			self.__dialog.createMessageDialog("\nDI-Alert service restarted.", 7, 50, "Notification Message")
			self.__logger.generateApplicationLog("DI-Alert service restarted", 1, "__service", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif int(result) == 1280:
			self.__dialog.createMessageDialog("\nFailed to restart DI-Alert service. Not found.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog("Failed to restart DI-Alert service. Not found.", 3, "__service", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		self.__action_to_cancel()


	def stopService(self):
		"""
		Method to stop the DI-Alert service.
		"""
		result = system("systemctl stop di-alert.service")
		if int(result) == 0:
			self.__dialog.createMessageDialog("\nDI-Alert service stopped.", 7, 50, "Notification Message")
			self.__logger.generateApplicationLog("DI-Alert service stopped", 1, "__service", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		elif int(result) == 1280:
			self.__dialog.createMessageDialog("\nFailed to stop DI-Alert service. Not found.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog("Failed to stop DI-Alert service. Not found.", 3, "__service", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG, user = self.__constants.USER, group = self.__constants.GROUP)
		self.__action_to_cancel()


	def getActualStatusService(self):
		"""
		Method to get the current status of the DI-Alert service.
		"""
		if path.exists("/tmp/di_alert.status"):
			remove("/tmp/di_alert.status")
		system('(systemctl is-active --quiet di-alert.service && echo "DI-Alert service is running!" || echo "DI-Alert service is not running!") >> /tmp/di_alert.status')
		system('echo "Detailed service status:" >> /tmp/di_alert.status')
		system('systemctl -l status di-alert.service >> /tmp/di_alert.status')
		with open_io("/tmp/di_alert.status", 'r', encoding = "utf-8") as status_file:
			self.__dialog.createScrollBoxDialog(status_file.read(), 15, 70, "DI-Alert Service")
		self.__action_to_cancel()