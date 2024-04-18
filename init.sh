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
sudo apt install mariadb-server

# Press Y

# Start mysql service, otherwise won't be able to login
sudo service mysql start

# # Open mysql with sudo permission, not using username, password for now.
# sudo mysql

# MySQL connection details
MYSQL_USER="root"
MYSQL_PASSWORD="hv7460"
MYSQL_HOST="localhost"
MYSQL_DATABASE="Library"

# MySQL command to create database
CREATE_DB_QUERY="CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Execute Mysql command, -e means next arg will be a sql query, "$CREATE_DB_QUERY" will be replaced by value from SHELL Variable.
sudo mysql -e "$CREATE_DB_QUERY"


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