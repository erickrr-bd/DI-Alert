#! /usr/bin/env python3

from modules.DI_Alert_Agent_Class import DIAlertAgent

"""
Attribute that stores an object of the DIAlertAgent class.
"""
di_alert_agent = DIAlertAgent()

"""
Main function of the application
"""
if __name__ == "__main__":
	di_alert_agent.startDIAlertAgent()