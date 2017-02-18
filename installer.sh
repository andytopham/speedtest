#!/bin/bash
# Installer for broadband speedtest.
# Sets up for using google spreadsheet logging and lcd display and speedtest application.
echo 'Setting up for broadband speedtest'
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
echo "apt-get installs"
apt-get update
pip install gspread
pip install speedtest-cli
# git clone git://github.com/andytopham/lib.git
echo "--------------------------------------"
echo "You still need to copy the authorisation file across."
echo "--------------------------------------"
echo "Finished speedtest setup."
