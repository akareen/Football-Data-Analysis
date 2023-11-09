#!/bin/bash

# Exit the script if any command fails
set -e

# Setting up the virtual display
sudo apt-get update
sudo apt-get install -y xvfb x11-utils python3-pyqt5

# Install Google Chrome
sudo apt-get install -y google-chrome-stable

# Install wget and unzip if they are not installed
sudo apt-get install -y wget unzip

# Get the latest ChromeDriver version number
CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+\.\d+")
CHROME_DRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")

# Install ChromeDriver
wget -N "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

# Installing the required Python packages
pip3 install pyvirtualdisplay selenium pyautogui bs4 requests pandas

# Check the installation status
if [ $? -eq 0 ]; then
    echo "Installation successful"
else
    echo "Installation failed"
    exit 1
fi
