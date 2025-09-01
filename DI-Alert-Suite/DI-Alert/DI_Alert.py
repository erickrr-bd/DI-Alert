#! /usr/bin/env python3.12

"""
Main method.
"""
from modules.DI_Alert_Class import DIAlert

if __name__ == "__main__":	
		di_alert = DIAlert()
		di_alert.run_as_daemon()
