#! /bin/bash

# Date: 27/08/2025
# Author: Erick Roberto Rodriguez Rodriguez
# Installation script.

# Usage: $ ./di_alert_installer.sh

clear

# Function that prints a banner.
banner()
{
	echo "+------------------------------------------+"
  	printf "| %-40s |\n" "`date`"
  	echo "|                                          |"
  	printf "|`tput bold` %-40s `tput sgr0`|\n" "$@"
  	echo "+------------------------------------------+"
}

# Application folders and files.
BASE_DIR=/etc/DI-Alert-Suite
DI_ALERT_CONFIGURATION=/etc/DI-Alert-Suite/DI-Alert/configuration
DI_ALERT_AGENT_CONFIGURATION=/etc/DI-Alert-Suite/DI-Alert-Agent/configuration
DI_ALERT_LOGS=/var/log/DI-Alert
DI_ALERT_KEY=/etc/DI-Alert-Suite/DI-Alert/configuration/key

# Print banner
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "
  _____ _____             _           _   
 |  __ \_   _|      /\   | |         | |  
 | |  | || |______ /  \  | | ___ _ __| |_ 
 | |  | || |______/ /\ \ | |/ _ \ '__| __|
 | |__| || |_    / ____ \| |  __/ |  | |_ 
 |_____/_____|  /_/    \_\_|\___|_|   \__|v3.2                                          
"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo -e "[*] Author: Erick Roberto Rodriguez Rodriguez"
echo -e "[*] Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com"
echo -e "[*] GitHub: https://github.com/erickrr-bd/DI-Alert"
echo -e "[*] Installer for DI-Alert v3.2 - August 2025\n"

echo "Do you want to install or update DI-Alert? (I/U)"
read opc

if [ $opc = "I" ] || [ $opc = "i" ]; then
	# "di_alert" user and group creation.
	banner "Creating user and group"
	echo ''
	if grep -w ^di_alert /etc/group > /dev/null; then
		echo -e "[*] \e[0;31m\"di_alert\" group already exists\e[0m"
	else
		groupadd di_alert
		echo -e "[*] \e[0;32m\"di_alert\" group created\e[0m"
	fi
	if id di_alert &> /dev/null; then
		echo -e "[*] \e[0;31m\"di_alert\" user already exists\e[0m\n"
	else
		useradd -M -s /bin/nologin -g di_alert -d /opt/DI-Alert-Suite di_alert
		echo -e "[*] \e[0;32m\"di_alert\" user created\e[0m\n"
	fi
	# Copy directories and files.
	banner "Installing DI-Alert"
	echo ''
	cp -r DI-Alert-Suite /opt
	echo -e "[*] \e[0;32mInstallation completed\e[0m\n"
	# Creation of folders and files.
	banner "Creation of folders and files"
	echo ''
	mkdir -p $DI_ALERT_CONFIGURATION
	mkdir -p $DI_ALERT_AGENT_CONFIGURATION
	mkdir -p $DI_ALERT_LOGS
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $DI_ALERT_KEY
$encryption_key
EOF
	echo -e "[*] \e[0;32mFolders and files created\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	chown di_alert:di_alert -R $BASE_DIR
	find "$BASE_DIR" -type f -exec chmod 640 {} \;
	find "$BASE_DIR" -type d -exec chmod 750 {} \;
	chown di_alert:di_alert -R /opt/DI-Alert-Suite
	find /opt/DI-Alert-Suite -type f -exec chmod 640 {} \;
	find /opt/DI-Alert-Suite -type d -exec chmod 750 {} \;
	chmod u=rwx,g=rx,o= /opt/DI-Alert-Suite/DI-Alert/DI_Alert.py
	chmod u=rwx,g=rx,o= /opt/DI-Alert-Suite/DI-Alert-Tool/DI_Alert_Tool.py
	chmod u=rwx,g=rx,o= /opt/DI-Alert-Suite/DI-Alert-Agent/DI_Alert_Agent.py
	chown di_alert:di_alert -R $DI_ALERT_LOGS
	chmod 750 $DI_ALERT_LOGS
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Creating services or daemons.
	banner "Creation of services for DI-Alert and DI-Alert-Agent"
	echo ''
	cp di-alert.service /etc/systemd/system/
	cp di-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	systemctl enable di-alert.service
	systemctl enable di-alert-agent.service
	echo ''
	echo -e "[*] \e[0;32mServices created\e[0m\n"
	# Creating aliases.
	banner "Creating aliases for DI-Alert-Tool"
	echo ''
	echo "alias DI-Alert-Tool='/opt/DI-Alert-Suite/DI-Alert-Tool/DI_Alert_Tool.py'" >> ~/.bashrc
	echo -e "[*] \e[0;32mCreated alias\e[0m\n"
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	# Stop services or daemons.
	banner "Stopping services"
	echo ''
	systemctl stop di-alert.service
	systemctl stop di-alert-agent.service
	echo -e "[*] \e[0;32mServices stopped\e[0m\n"
	# Copy directories and files.
	banner "Updating DI-Alert"
	echo ''
	cp -r DI-Alert-Suite /opt
	echo -e "[*] \e[0;32mUpdate completed\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	chown di_alert:di_alert -R /opt/DI-Alert-Suite
	find /opt/DI-Alert-Suite -type f -exec chmod 640 {} \;
	find /opt/DI-Alert-Suite -type d -exec chmod 750 {} \;
	chmod u=rwx,g=rx,o= /opt/DI-Alert-Suite/DI-Alert/DI_Alert.py
	chmod u=rwx,g=rx,o= /opt/DI-Alert-Suite/DI-Alert-Tool/DI_Alert_Tool.py
	chmod u=rwx,g=rx,o= /opt/DI-Alert-Suite/DI-Alert-Agent/DI_Alert_Agent.py
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Start services or daemons.
	banner "Starting DI-Alert and DI-Alert-Agent services"
	echo ''
	systemctl start di-alert.service
	systemctl start di-alert-agent.service
	echo -e "[*] \e[0;32mServices started\e[0m\n"
else
	clear
	exit
fi 