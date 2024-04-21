# MySQL connection details
MYSQL_USER="web"
MYSQL_PASSWORD="webPass"
MYSQL_HOST="localhost"
MYSQL_DATABASE="LibraryManagementSystem"

sudo mysql << EOF
CREATE USER '$MYSQL_USER'@'$MYSQL_HOST' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON *.* to '$MYSQL_USER'@'$MYSQL_HOST';
CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
EOF

# MySQL command to create database
CREATE_DB_QUERY="CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Execute Mysql command, to execute your query -e means next arg will be a sql query, "$CREATE_DB_QUERY" will be replaced by value from SHELL Variable.
sudo mysql -e "$CREATE_DB_QUERY"

# Check DBs list, to verify creation of new DBs
sudo mysql -e "SHOW DATABASES;"

# MySQL command to create tables
CREATE_TABLE_QUERY_USERS="
CREATE TABLE IF NOT EXISTS $MYSQL_DATABASE.Users (
    UserId INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    StudentID INT,
    AdminID INT,
    UserType ENUM('Admin', 'Student'),
    Email VARCHAR(50),
    Password VARCHAR(50)
);"

sudo mysql -D$MYSQL_DATABASE -e "$CREATE_TABLE_QUERY_USERS"

# SQL keywords are case-insensitive but not Table,Columns,Key Names,etc
sudo mysql -e "USE $MYSQL_DATABASE; SELECT * FROM Users;"

# MySQL command to insert data into tables
INSERT_DATA_QUERY_USERS="
INSERT INTO $MYSQL_DATABASE.Users (UserId, StudentID, AdminID, UserType, Email, Password)
VALUES (1, NULL, 101, 'Admin', 'admin@example.com', 'admin_password'),
       (2, 101, NULL, 'Student', 'student@example.com', 'student_password');"
       
sudo mysql -D$MYSQL_DATABASE -e "$INSERT_DATA_QUERY_USERS"

USE_MYDB="USE $MYSQL_DATABASE;"
# WRITE SQL QUERIES before EOF block
sudo mysql << EOF
$USE_MYDB
SELECT * FROM Users;
CREATE TABLE IF NOT EXISTS $MYSQL_DATABASE.Books (
    BookId INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    BookTitle VARCHAR(255),
    BookAuthor VARCHAR(255),
    BookGenre VARCHAR(50),
    BookPublisher VARCHAR(255),
    BookYear INT,
    BookStatus ENUM('Available', 'On Hold', 'Not Available')
);

CREATE TABLE IF NOT EXISTS BookReservations (
    BookReservationId INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
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


INSERT INTO Books (BookId, BookTitle, BookAuthor, BookGenre, BookPublisher, BookYear, BookStatus) 
VALUES
(1, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'J.B. Lippincott & Co.', 1960, 'Not Available'),
(2, '1984', 'George Orwell', 'Dystopian Fiction', 'Secker & Warburg', 1949, 'On Hold'),
(3, 'The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 'Little, Brown and Company', 1951, 'Available'),
(4, 'Pride and Prejudice', 'Jane Austen', 'Classic Literature', 'T. Egerton, Whitehall', 1813, 'Available'),
(5, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic Literature', 'Scribner', 1925, 'Available'),
(6, 'Moby-Dick', 'Herman Melville', 'Adventure Fiction', 'Richard Bentley', 1851, 'Available'),
(7, 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'Allen & Unwin', 1954, 'Available'),
(8, 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'Allen & Unwin', 1937, 'Available'),
(9, 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Fantasy', 'Bloomsbury', 1997, 'Available'),
(10, 'The Adventures of Huckleberry Finn', 'Mark Twain', 'Adventure Fiction', 'Chatto & Windus', 1884, 'Available'),
(11, 'The Odyssey', 'Homer', 'Epic Poetry', 'Various', -700, 'Available'),
(12, 'The Great Expectations', 'Charles Dickens', 'Classic Literature', 'Chapman & Hall', 1861, 'Available'),
(13, 'Animal Farm', 'George Orwell', 'Political Satire', 'Secker & Warburg', 1945, 'Available'),
(14, 'The Adventures of Sherlock Holmes', 'Arthur Conan Doyle', 'Mystery', 'George Newnes Ltd', 1892, 'Available'),
(15, 'The Picture of Dorian Gray', 'Oscar Wilde', 'Gothic Fiction', 'Lippincott''s Monthly Magazine', 1890, 'Available'),
(16, 'Frankenstein', 'Mary Shelley', 'Gothic Fiction', 'Lackington, Hughes, Harding, Mavor & Jones', 1818, 'Available'),
(17, 'Don Quixote', 'Miguel de Cervantes', 'Novel', 'Francisco de Robles', 1605, 'Available'),
(18, 'Alice''s Adventures in Wonderland', 'Lewis Carroll', 'Fantasy', 'Macmillan', 1865, 'Available'),
(19, 'The War of the Worlds', 'H.G. Wells', 'Science Fiction', 'William Heinemann', 1898, 'Available'),
(20, 'Dracula', 'Bram Stoker', 'Gothic Horror', 'Archibald Constable and Company', 1897, 'Available'),
(21, 'War and Peace', 'Leo Tolstoy', 'Historical Fiction', 'The Russian Messenger', 1869, 'Available');


INSERT INTO BookReservations (BookReservationId, UserName, UserPhone, BookTitle, IssueDate, ReturnDate, UserId, BookId)
VALUES (1, 'John Doe', 1234567890, 'The Great Gatsby', '2024-04-18 10:00:00', '2024-04-25 10:00:00', 1, 1),
       (2, 'Jane Smith', 9876543210, 'To Kill a Mockingbird', '2024-04-20 14:00:00', '2024-04-27 14:00:00', 2, 2);

EOF

echo "Database setup completed successfully."


# Dropping the unwanted Attributes
USE_MYDB="USE $MYSQL_DATABASE;"
sudo mysql << EOF
$USE_MYDB
Alter Table Users DROP Column StudentID;
Alter Table Users DROP Column AdminID;
EOF

