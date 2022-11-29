#! /usr/bin/env python3

from modules.DI_Alert_Tool_Class import DIAlertTool

"""
Attribute that stores an object of the DIAlertTool class.
"""
di_alert_tool = DIAlertTool()

"""
Main function of the application
"""
if __name__ == "__main__":	
	while True:
		di_alert_tool.mainMenu()