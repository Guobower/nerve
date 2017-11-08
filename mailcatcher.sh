#!/usr/bin/env bash
#--------------------------------------------------
# Update Server
#--------------------------------------------------
echo -e "\n---- Update Server ----"
sudo apt-get update
sudo apt-get upgrade -y

#--------------------------------------------------
# Install Mail Catcher
#--------------------------------------------------
echo -e "\n---- Install Mail Catcher ----"
sudo apt-get install -y build-essential checkinstall
sudo apt-get install -y libsqlite3-dev ruby2.0 ruby2.0-dev
sudo gem2.0 install mailcatcher

#--------------------------------------------------
# Create Startup Script for Mail Catcher
#--------------------------------------------------
echo -e "\n---- Create Startup for Mail Catcher ----"
cat <<EOT > /etc/init/mailcatcher.conf
description "Mailcatcher"
start on runlevel [2345]
stop on runlevel [!2345]
respawn
exec /usr/bin/env $(which mailcatcher) --foreground --http-ip=0.0.0.0 --smtp-ip=0.0.0.0
EOT

sudo service mailcatcher start
