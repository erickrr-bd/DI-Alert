#! /bin/bash

clear
echo -e '\e[1;33m--------------------------------------------------------------------------------\e[0m'
echo -e "\e[96m@2022 Tekium. All rights reserved.\e[0m"
echo -e '\e[96mInstaller for DI-Alert v3.1\e[0m'
echo -e '\e[96mAuthor: Erick Rodríguez\e[0m'
echo -e '\e[96mEmail: erodriguez@tekium.mx, erickrr.tbd93@gmail.com\e[0m'
echo -e '\e[96mLicense: GPLv3\e[0m'
echo -e '\e[1;33m--------------------------------------------------------------------------------\e[0m'
echo ''
echo 'Do you want to install or update DI-Alert on the computer (I/U)?'
read opc

#Absolute paths that must be created for DI-Alert to work
path_di_alert_configuration=/etc/DI-Alert-Suite/DI-Alert/configuration
path_di_alert_agent_configuration=/etc/DI-Alert-Suite/DI-Alert-Agent/configuration
path_di_alert_logs=/var/log/DI-Alert

#DI-Alert installation
if [ $opc = "I" ] || [ $opc = "i" ]; then
	echo ''
	echo -e '\e[96mStarting the DI-Alert installation...\e[0m'
	echo ''
	echo 'Do you want to install the packages and libraries necessary for the operation of DI-Alert (Y/N)?'
	read opc_lib
	if [ $opc_lib = "Y" ] || [ $opc_lib = "y" ]; then
		echo ''
		echo -e '\e[96mStarting the installation of the required packages and libraries...\e[0m'
		yum install python3-pip -y
		dnf install dialog -y
		dnf install gcc -y
		dnf install python3-devel -y
		dnf install libcurl-devel -y
		dnf install openssl-devel -y
		pip3 install pythondialog 
		pip3 install pycryptodome
		pip3 install pyyaml 
		pip3 install pycurl 
		pip3 install requests 
		echo ''
		echo -e '\e[96mRequired installed libraries...\e[0m'
		sleep 3
		echo ''
	fi
	echo -e '\e[96mCreating user and group for DI-Alert...\e[0m'
	groupadd di_alert
	useradd -M -s /bin/nologin -g di_alert -d /etc/DI-Alert-Suite di_alert
	echo ''
	echo -e '\e[96mUser and group created...\e[0m'
	sleep 3
	echo ''
	#Creation of daemons for DI-Alert and DI-Alert-Agent
	echo -e '\e[96mCreating the daemon for DI-Alert and DI-Alert-Agent\e[0m'
	dir=$(sudo pwd)
	cd $dir
	cp di-alert.service /etc/systemd/system/
	cp di-alert-agent.service /etc/systemd/system
	systemctl daemon-reload
	systemctl enable di-alert.service
	systemctl enable di-alert-agent.service
	echo ''
	echo -e '\e[96mDaemons created\e[0m'
	sleep 3
	echo ''
	#Copy of necessary files and folders for DI-Alert operation 
	echo -e '\e[96mCopying and creating the necessary files and folders\e[0m'
	echo ''
	cp -r DI-Alert-Suite /etc/
	if [ ! -d "$path_di_alert_configuration" ]; 
	then
		mkdir -p $path_di_alert_configuration
	fi
	if [ ! -d "$path_di_alert_agent_configuration" ]; 
	then
		mkdir -p $path_di_alert_agent_configuration
	fi
	if [ ! -d "$path_di_alert_logs" ]; 
	then
		mkdir -p $path_di_alert_logs
	fi
	chown di_alert:di_alert -R /etc/DI-Alert-Suite
	chown di_alert:di_alert -R /var/log/DI-Alert
	echo -e '\e[96mFiles and folders copied and created\e[0m'
	sleep 3
	echo ''
	#Passphrase creation
	echo -e '\e[96mCreating passphrase\e[0m'
	passphrase=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > /etc/DI-Alert-Suite/DI-Alert/configuration/key 
$passphrase
EOF
	echo ''
	echo -e '\e[96mPassphrase created\e[0m'
	sleep 3
	echo ''
	#Alias creation
	echo -e '\e[96mCreating alias for DI-Alert-Tool\e[0m'
	alias DI-Alert-Tool='/etc/DI-Alert-Suite/DI-Alert-Tool/DI_Alert_Tool.py'
	sleep 3
	echo ''
	echo -e '\e[96mAlias created\e[0m'
	echo ''
	echo -e '\e[96mDI-Alert has been installed\e[0m'
	sleep 3	
	#DI-Alert-Tool execution
	echo ''
	echo -e '\e[96mStarting DI-Alert-Tool\e[0m'
	sleep 3
	cd /etc/DI-Alert-Suite/DI-Alert-Tool
	python3 DI_Alert_Tool.py
#DI-Alert update
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	echo ''
	echo -e '\e[96mStarting the VulTek-Alert update\e[0m'
	echo ''
	echo -e '\e[96mStopping the vultek-alert daemon\e[0m'
	dir=$(sudo pwd)
	systemctl stop vultek-alert.service
	cp vultek-alert.service /etc/systemd/system/
	cp vultek-alert-agent.service /etc/systemd/system/
	systemctl daemon-reload
	echo ''
	echo -e '\e[96mDaemon updated\e[0m'
	sleep 3
	echo ''
	echo -e '\e[96mUpdating application components\e[0m'
	#rm -rf /etc/VulTek-Alert-Suite
	cp -r VulTek-Alert-Suite /etc/
	if [ ! -d "$vultek_alert_configuration" ]; 
	then
		mkdir $vultek_alert_configuration
	fi
	if [ ! -d "$vutek_alert_agent_configuration" ]; 
	then
		mkdir $vutek_alert_agent_configuration
	fi
	if [ ! -d "$vultek_alert_database" ]; 
	then
		mkdir $vultek_alert_database
	fi
	chown vultek_alert:vultek_alert -R /etc/VulTek-Alert-Suite
	echo ''
	echo -e '\e[96mApplication components updated\e[0m'
	sleep 3
	echo ''
	echo -e '\e[96mUpdate finished\e[0m'
	echo ''
	echo -e '\e[96mStarting VulTek-Alert-Tool\e[0m'
	sleep 3
	cd /etc/VulTek-Alert-Suite/VulTek-Alert-Tool
	python3 VulTek_Alert_Tool.py
else
	clear
	exit
fi 