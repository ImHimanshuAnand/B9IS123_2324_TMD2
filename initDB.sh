# MySQL connection details
MYSQL_USER="root"
MYSQL_PASSWORD="hv7460"
MYSQL_HOST="localhost"
MYSQL_DATABASE="Lib6"

# MySQL command to create database
CREATE_DB_QUERY="CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Execute Mysql command, to execute your query -e means next arg will be a sql query, "$CREATE_DB_QUERY" will be replaced by value from SHELL Variable.
sudo mysql -e "$CREATE_DB_QUERY"

# Check DBs list, to verify creation of new DBs
sudo mysql -e "SHOW DATABASES;"

# MySQL command to create tables
CREATE_TABLE_QUERY_USERS="
CREATE TABLE IF NOT EXISTS $MYSQL_DATABASE.Users (
    UserId INT PRIMARY KEY,
    StudentID INT,
    AdminID INT,
    UserType ENUM('Admin', 'Student'),
    Email VARCHAR(50),
    Password VARCHAR(50)
);"

# -uUSER, -pPASSWORD, -tTABLEFORMAT, -DDBNAME
# -D flag is for selecting which database to use, just like "USE <database_name>; , $SHELLVARNAME is replaced by value of shell variable"
# else this error -> ERROR 1046 (3D000) at line 1: No database selected
sudo mysql -D$MYSQL_DATABASE -e "$CREATE_TABLE_QUERY_USERS"

# SQL keywords are case-insensitive but not Table,Columns,Key Names,etc
sudo mysql -e "USE Lib6; SELECT * FROM Users;"
sudo mysql -t -e "USE $MYSQL_DATABASE; SELECT Email FROM Users;"

# To Check Table Schema, DESC <TableName> or DESCRIBE <TableName>
sudo mysql -e "USE $MYSQL_DATABASE; DESCRIBE Users;"