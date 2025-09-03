#! /usr/bin/env python3.12

"""
Main method.
"""
from modules.DI_Alert_Agent_Class import DIAlertAgent

if __name__ == "__main__":
	di_alert_agent = DIAlertAgent()
	di_alert_agent.run_as_daemon()
