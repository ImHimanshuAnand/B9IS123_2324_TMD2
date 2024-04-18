#! /bin/sh

# Update repo list
sudo apt update

# Install Virtual env
python3 -m venv venv

# Activate Virtual env
source venv/bin/activate

# Install Flask dependency
pip3 install Flask

# Install MariaDB
sudo apt install mariadb-server --yes

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