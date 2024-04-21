from flask import Blueprint, request, render_template, jsonify
import mysql.connector

books_bp = Blueprint('books', __name__)

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'web',
    'password': 'webPass',
    'database': 'LibraryManagementSystem'
}

# Function to establish MySQL connection
def get_db():
    return mysql.connector.connect(**db_config)

# Define books endpoint, Books APIs
@books_bp.route('/books',methods=["GET"])
def get_books():
  # Get sort parameters from query string
  sort_by = request.args.get('sort_by', default='BookId')
  sort_order = request.args.get('sort_order', default='asc')
  filter_param = request.args.get('filter_param', default=None)
  filter_value = request.args.get('filter_value', default=None)
  search_by = request.args.get('search_by', default=None)
  search_value = request.args.get('search_value', default=None)
  print(request.args)
  # Construct SQL query based on parameters
  sql_query = "SELECT * FROM Books WHERE 1=1"
  if filter_param and filter_value:
    sql_query += f" AND {filter_param} = '{filter_value}'"
  if search_by and search_value:
    sql_query += f" AND {search_by} LIKE '%{search_value}%'"
  # Sort by title
  if sort_by and sort_order:
    sql_query += f" ORDER BY {sort_by} {sort_order}"
  # DB connection
  db = get_db()
  cursor = db.cursor()
  # Execute the SQL query
  cursor.execute(sql_query)
  print(sql_query)
  # Fetch the results
  books_data = cursor.fetchall()
  db.commit()
  db.close()
  # Convert the results to a list of dictionaries
  books_list = []
  for book in books_data:
      print(book[0])
      book_dict = {
          'BookId': book[0],
          'BookTitle': book[1],
          'BookAuthor': book[2],
          'BookGenre': book[3],
          'BookPublisher': book[4],
          'BookYear': book[5],
          'BookStatus': book[6],
      }
      books_list.append(book_dict)
  # print(books_data,books_list)
  return jsonify(books_list)
  # return render_template("book_list.html", books=books_list)


@books_bp.route('/books/<int:BookId>',methods=["GET"])
def get_book_by_id(BookId):
  db = get_db()
  cursor = db.cursor()
  cursor.execute("SELECT * FROM Books WHERE BookId = %s",(BookId,))
  books = cursor.fetchone()
  db.commit()
  db.close()
  print(books)
  return jsonify(books)

@books_bp.route('/books',methods=["POST"])
def add_book():
    print(request.form)
    BookTitle=request.form.get('BookTitle')
    BookAuthor=request.form['BookAuthor']
    BookGenre=request.form['BookGenre']
    BookPublisher=request.form['BookPublisher']
    BookYear=request.form['BookYear']
    BookStatus=request.form['BookStatus']    
    print(request.form)
    
    db = get_db()
    cursor = db.cursor()
    query= '''INSERT INTO Books (BookTitle,BookAuthor,BookGenre,BookPublisher,BookYear,BookStatus) VALUES('{}','{}','{}','{}','{}','{}');'''.format(BookTitle,BookAuthor,BookGenre,BookPublisher,BookYear,BookStatus)
    cursor.execute(query)
    db.commit()
    db.close()
    return jsonify({'message': 'Book Added successfully'})

@books_bp.route('/books/<int:BookId>', methods=['PUT'])
def update_book(BookId):
  BookTitle=request.form.get('BookTitle')
  BookAuthor=request.form.get('BookAuthor')
  BookGenre=request.form.get('BookGenre')
  BookPublisher=request.form.get('BookPublisher')
  BookYear=request.form.get('BookYear')
  BookStatus=request.form.get('BookStatus')    
  print(request.form)
  # Construct SQL query to update the book
  sql_query = "UPDATE Books SET"
  if BookTitle:
    sql_query += f" BookTitle = '{BookTitle}',"
  if BookAuthor:
    sql_query += f" BookAuthor = '{BookAuthor}',"
  if BookGenre:
    sql_query += f" BookGenre = '{BookGenre}',"
  if BookPublisher:
    sql_query += f" BookPublisher = '{BookPublisher}',"
  if BookYear:
    sql_query += f" BookYear = '{BookYear}',"
  if BookStatus:
    sql_query += f" BookStatus = '{BookStatus}',"
  # Remove trailing comma
  sql_query = sql_query[:-1]
  sql_query += f" WHERE BookId = {BookId}"
  # Execute SQL query
  print(sql_query)
  db = get_db()
  cursor = db.cursor()
  cursor.execute(sql_query)
  db.commit()
  db.close()
  return jsonify({'message': 'Book Updated successfully'})

@books_bp.route('/books/<int:BookId>', methods=["DELETE"])
def delete_book(BookId):
  try:
    print(BookId)
    db = get_db()
    cursor = db.cursor()
    
    # mysql module, cursor.execute requires a sql query and a tuple as parameters, so keep , at end
    books = cursor.execute("DELETE FROM Books WHERE BookId = %s", (BookId,))
    db.commit()
    db.close()
    return jsonify({'message': 'Book deleted successfully'})
  except Exception as e:
    print('Error:', e)
    # return jsonify({'message': Exception})
    return jsonify({'error': 'Internal server error', 'message':str(e)}), 404
   
