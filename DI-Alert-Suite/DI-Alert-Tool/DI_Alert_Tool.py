#! /usr/bin/env python3.12

"""
Main function.
"""
from modules.DI_Alert_Tool_Class import DIAlertTool

if __name__ == "__main__":
	di_alert_tool = DIAlertTool()
	while True:
		di_alert_tool.main_menu()
