#!/usr/bin/env bash
#--------------------------------------------------
# Update Server
#--------------------------------------------------
echo -e "\n---- Update Server ----"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential checkinstall
sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
                    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
                    zlib1g-dev

#--------------------------------------------------
# Install Python 3.6.3
#--------------------------------------------------
echo -e "\n---- Install Python 3.6.3 ----"
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xvf Python-3.6.3.tar.xz
cd Python-3.6.3
./configure
sudo make altinstall

#--------------------------------------------------
# Install Dependencies
#--------------------------------------------------
echo -e "\n---- Install Python Dependency ----"
sudo pip3.6 install psutil==5.4.0 cryptography==2.1.3

