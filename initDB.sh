# MySQL connection details
MYSQL_USER="web"
MYSQL_PASSWORD="webPass"
MYSQL_HOST="localhost"
MYSQL_DATABASE="Library1"

sudo mysql << EOF
CREATE USER '$MYSQL_USER'@'$MYSQL_HOST' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON *.* to '$MYSQL_USER'@'$MYSQL_HOST';
CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
EOF

# INCREMENTING Database Count of MYSQL_DATABASE to avoid below error.
# ERROR 1062 (23000) at line 2: Duplicate entry '1' for key 'PRIMARY'

# MySQL command to create database
CREATE_DB_QUERY="CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Execute Mysql command, to execute your query -e means next arg will be a sql query, "$CREATE_DB_QUERY" will be replaced by value from SHELL Variable.
sudo mysql -e "$CREATE_DB_QUERY"

# Check DBs list, to verify creation of new DBs
sudo mysql -e "SHOW DATABASES;"

# MySQL command to create tables
CREATE_TABLE_QUERY_USERS="
CREATE TABLE IF NOT EXISTS $MYSQL_DATABASE.Users (
    UserId INT PRIMARY KEY AUTO_INCREMENT,
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
sudo mysql -e "USE $MYSQL_DATABASE; SELECT * FROM Users;"
# Todo: not printing tables to script's output even after 4-5 attempts
sudo mysql -t -e "USE $MYSQL_DATABASE; SELECT Email FROM Users;"

# To Check Table Schema, DESC <TableName> or DESCRIBE <TableName>
sudo mysql -e "USE $MYSQL_DATABASE; DESCRIBE Users;"

# MySQL command to insert data into tables
INSERT_DATA_QUERY_USERS="
INSERT INTO $MYSQL_DATABASE.Users (UserId, StudentID, AdminID, UserType, Email, Password)
VALUES (1, NULL, 101, 'Admin', 'admin@example.com', 'admin_password'),
       (2, 101, NULL, 'Student', 'student@example.com', 'student_password');"
       
sudo mysql -D$MYSQL_DATABASE -e "$INSERT_DATA_QUERY_USERS"

# echo "select value1, value2 from table" | mysql -uUSER -pPASS | column -t
# echo "select * from table" | mysql -uUSER -pPASS | column -t
echo "USE $MYSQL_DATABASE; select * from Users" | sudo mysql | column -t
# Successfully Prints Table data onto terminal output after 3-4 attempts

USE_MYDB="USE $MYSQL_DATABASE;"
# WRITE SQL QUERIES before EOF block
sudo mysql << EOF
$USE_MYDB
SELECT * FROM Users;
CREATE TABLE IF NOT EXISTS $MYSQL_DATABASE.Books (
    BookId INT PRIMARY KEY,
    BookTitle VARCHAR(255),
    BookAuthor VARCHAR(255),
    BookGenre VARCHAR(50),
    BookPublisher VARCHAR(255),
    BookYear DATE,
    BookStatus ENUM('Available', 'On Hold', 'Not Available')
);

CREATE TABLE IF NOT EXISTS BookReservations (
    BookReservationId INT PRIMARY KEY,
    UserName VARCHAR(50),
    UserPhone BIGINT(10),
    BookTitle VARCHAR(255),
    IssueDate DATETIME,
    ReturnDate DATETIME,
    UserId INT,
    BookId INT,
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    FOREIGN KEY (BookId) REFERENCES Books(BookId)
);

ALTER TABLE Books AUTO_INCREMENT=5001;
ALTER TABLE BookReservations AUTO_INCREMENT=1001;


INSERT INTO Books (BookId, BookTitle, BookAuthor, BookGenre, BookPublisher, BookYear, BookStatus)
VALUES (1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 'Scribner', '1925-04-10', 'Available'),
       (2, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'J. B. Lippincott & Co.', '1960-07-11', 'Available'),
       (3, '1984', 'George Orwell', 'Dystopian', 'Secker & Warburg', '1949-06-08', 'On Hold');

INSERT INTO BookReservations (BookReservationId, UserName, UserPhone, BookTitle, IssueDate, ReturnDate, UserId, BookId)
VALUES (1, 'John Doe', 1234567890, 'The Great Gatsby', '2024-04-18 10:00:00', '2024-04-25 10:00:00', 1, 1),
       (2, 'Jane Smith', 9876543210, 'To Kill a Mockingbird', '2024-04-20 14:00:00', '2024-04-27 14:00:00', 2, 2);

EOF

# ERROR 1046 (3D000) at line 1: No database selected
# SOLVED: USE <dbName>; before queries

# ERROR 1049 (42000) at line 3: Unknown database '$MYSQL_DATABASE'
# ERROR 1049 (42000) at line 1: Unknown database '${MYSQL_DATABASE}'
# ERROR 1064 (42000) at line 1: You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '$USE_MYDB
# SOLVED: replaced double quoted "EOF" to wihout quotes EOF

echo "Database setup completed successfully."

# to run scripts
# source command (which is an alias for .)
# example: 
# . test.sh
# source test.sh



# Dropping the unwanted Attributes
USE_MYDB="USE $MYSQL_DATABASE;"
# WRITE SQL QUERIES before EOF block
sudo mysql << EOF
$USE_MYDB
Alter Table Users DROP Column StudentID;
Alter Table Users DROP Column AdminID;
EOF

