#! /bin/sh

AZUREVM_HOSTNAME="library1.northeurope.cloudapp.azure.com"

sudo apt update # Update repo list
sudo  apt -y upgrade
sudo apt -y install python3-pip
pip3 install flask
pip3 install flask_login
pip3 install flask_bcrypt

sudo apt -y install apache2 python3-certbot-apache # Setup SSL certificate for https
sudo certbot --apache --himanshuhome1@gmail.com --A --N --$AZUREVM_HOSTNAME --1
sudo cp /etc/letsencrypt/live/$AZUREVM_HOSTNAME/cert.pem .
sudo cp /etc/letsencrypt/live/$AZUREVM_HOSTNAME/privkey.pem .
sudo chown `whoami` *.pem

sudo apt -y install mariadb-server # mariadb-client libmariadbclient-dev
pip3 install flask_cors mysql-connector-python
# sudo mysql

# Start mysql service, otherwise won't be able to login
sudo service mysql start

echo "After exit"
echo "Call another script here to setup DB"

bash ./initDB.sh
echo "Finished Running initDB.sh................"