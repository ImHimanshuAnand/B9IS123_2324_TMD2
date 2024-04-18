# MySQL connection details
MYSQL_USER="root"
MYSQL_PASSWORD="hv7460"
MYSQL_HOST="localhost"
MYSQL_DATABASE="Lib2"

# MySQL command to create database
CREATE_DB_QUERY="CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Execute Mysql command, -e means next arg will be a sql query, "$CREATE_DB_QUERY" will be replaced by value from SHELL Variable.
sudo mysql -e "$CREATE_DB_QUERY"

# Check DBs list, to verify creation of new DBs
sudo mysql -e "SHOW DATABASES;"