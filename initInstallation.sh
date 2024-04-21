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

# python3 -m venv venv # Install Virtual env
# source venv/bin/activate # Activate Virtual env
# pip3 install Flask # Install Flask dependency
# sudo apt install mariadb-server --yes # Install MariaDB


# Press Y or use "yes" command
# yes
# Infinite yes, with plain "yes" cmd, refer man yes
# Solved: append --varName1 --varName2 at end of command
# LOST the terminal output in codespaces prior to that, till Lib18 maybe.

# Start mysql service, otherwise won't be able to login
sudo service mysql start

# # Open mysql with sudo permission, not using username, password for now.
# sudo mysql

# # EXPORT DB
# sudo mysqldump Library > data-dump.sql

# # STEPS to IMPORT DB 
# sudo mysql << "EOF"
# CREATE DATABASE Lib1;
# SHOW DATABASES;
# EOF
# # CMD IMPORT DB
# sudo mysql -u root -p Lib1 < data-dump.sql

# # 
echo "After exit"
echo "Call another script here to setup DB"

bash ./initDB.sh
echo "Finished Running initDB.sh................"