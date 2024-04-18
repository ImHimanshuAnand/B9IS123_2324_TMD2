#! /bin/sh

# Install Virtual env
python3 -m venv venv
# Activate Virtual env
source venv/bin/activate
# Install Flask dependency
pip3 install Flask

# exit
# python3 app.py

sudo apt update
sudo apt install mariadb-server
# Press Y
sudo service mysql start
sudo mysql

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