from flask import Flask, render_template, request,redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
import mysql.connector
from flask_cors import CORS
import json

# MySQL Database Connection
mysql = mysql.connector.connect(
  user='web', 
  password='webPass',
  host='localhost',
  database='LibraryManagementSystem'
)

# # MySQL connection configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'web',
#     'password': 'webPass',
#     'database': 'LibraryManagementSystem'
# }

# Function to establish MySQL connection
# def get_db():
#     return mysql.connector.connect(**db_config)


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


# Flask app initialization 
app = Flask(__name__)
app.secret_key = 'Library_Management_secret_key'
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User class for Flask-Login 
Class Users(UserMixin):
   def __init__(self,UserID,UserType,Email):
      self.id = UserID
      self.UserType = UserType
      self.Email =  Email

#Loader Function for Flask Login
@login_manager.user_loader
def load_user(UserID):
  user = query_user_by_id(UserID)
  if user:
    return user
  else:
    return None 

# Database query function to get user by ID 
def query_user_by_id(UserID):
     select_query = 'SELECT * FROM Users WHERE UserID = %s '
     cursor = mysql.cursor()
     cursor.execute(select_query,(UserID))
     user = cursor.fetchone()

     if user:
      return Users(user[0],user[1],user[2])
     else:
      return None 


#Route for user signup
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    signup_alert = None
    if request.method == 'POST':
       UserType = request.form['UserType']
       Email = request.form['Email']
       Password = request.form['Password']
       print(UserType,Email,Password)

       hashed_password = bcrypt.genarate_password_hash(Password)

       cursor = mysql.cursor();
       insert_query= ''' INSERT INTO Users (UserType, Email, Password) VALUES('{}','{}','{}');'''.format(UserType,Email,Password)
       app.logger.info(insert_query)
       cursor.execute(insert_query)
       mysql.commit()

       flash("Signup successfull! Please Login.", "success")
       signup_alert = "Signup successfull! Please wait a moment."    
       return render_template('login.html', signup_alert=signup_alert)
    else:   
       return render_template('signup.html')
  
# Route for user login
@app.route("/login" ,methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
       UserType = request.form['UserType']
       Email = request.form['Email']
       Password = request.form['Password']

       cursor = mysql.cursor();
       select_query = '''SELECT * FROM Users WHERE UserType='{}' AND Email='{}';'''
       app.logger.info(select_query)
       cursor.execute(select_query, (UserType, Email))
       user = cursor.fetchone()
       if user and bcrypt.check_password_hash(user[3], Password):
          session['UserID'] = user[0]
          session['UserType'] = user[1]
          session['Email'] = user[2]
          
          login_user(Users(user[0],user[1],user[2]))

          if session['UserType'] == 'Admin':
            return redirect(url_for('add_book'));
          else:
            return redirect(url_for('book'));
       else:
          return 'INVALID USERNAME OR PASSWORD'

     return render_template('login.html')





@app.route("/")
def main():
  return "Hello, The app is started!"

@app.route('/book',methods=["GET","POST","PUT","DELETE"])
def book():
  if request.method == 'POST':
    # data = request.json
    # title = data['title']
    # print(title,author)
    # BookId=request.form['BookId']
    BookTitle=request.form['BookTitle']
    BookAuthor=request.form['BookAuthor']
    BookGenre=request.form['BookGenre']
    BookPublisher=request.form['BookPublisher']
    BookYear=request.form['BookYear']
    BookStatus=request.form['BookStatus']    
    # print(BookId)
    
    db = get_db()
    cursor = db.cursor()
    query= '''INSERT INTO Books (BookId,BookTitle,BookAuthor,BookGenre,BookPublisher,BookYear,BookStatus) VALUES('{}','{}','{}','{}','{}','{}','{}');'''.format(100,BookTitle,BookAuthor,BookGenre,BookPublisher,BookYear,BookStatus)
    cursor.execute(query)
    db.commit()
    db.close()
    return jsonify({'message': 'Book created successfully'})
  elif request.method == "PUT":
    books.append(request.get_json())
  elif request.method == "DELETE":
    print(request.view_args('book_id'))
    book_id=request.args.get('book_id')
    # book_id=request.args.get('book_id')
    db = get_db()
    cursor = db.cursor()
    books = cursor.execute("DELETE FROM Books WHERE id = %s", (100))
    db.commit()
    db.close()
    return jsonify({'message': 'Book deleted successfully'})
  elif request.method == "GET":
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    db.commit()
    db.close()
    return jsonify(books)
  else:
    return "UNKNOWN HTTP METHOD"

@app.route("/add_book", methods=['POST'])
def AddBook():
  if request.method == 'POST':
      BookId=request.form['BookId']
      BookTitle=request.form['BookTitle']
      BookAuthor=request.form['BookAuthor']
      BookGenre=request.form['BookGenre']
      BookPublisher=request.form['BookPublisher']
      BookYear=request.form['BookYear']
      BookStatus=request.form['BookStatus']
      print(BookTitle)
      cursor = mysql.cursor();
      insert_query= ''' INSERT INTO Books (BookId,BookTitle,BookAuthor,BookGenre,BookPublisher,BookYear,BookStatus) VALUES('{}','{}','{}');'''.format(BookId,BookTitle,BookAuthor,BookGenre,BookPublisher,BookYear,BookStatus)
      app.logger.info(insert_query)
      cursor.execute(insert_query)
      mysql.commit()
      flash("Successfully Inserted A Book into DB", "success")
      return jsonify(isError= False,
                message= "Success",
                statusCode= 200,
                # data= data
                ) 
      200
      #  return render_template('signup.html',"Success: Added a book!")
  # else:   
      #  return render_template('signup.html')


# @app.route("/userreservation")#URL leading to method
# def userreservation(): # Name of the method
#     if request.method == 'POST':
#       room_type = request.form['room_type']
#       check_in_date = request.form['room_type']
#       check_out_date = request.form['check_out_date']
#       return render_template('reservation_confirmation.html',room_type=room_type)
#     else:
#       return render_template('user_form.html') 

# @app.route("/adminform")#URL leading to method
# def adminform(): # Name of the method
#     if request.method == 'POST':
#        titleID = request.form['titleID']
#        title = request.form['title']
#        author = request.form['author']
#        genre = request.form['genre']
#        pulisher = request.form['year']
#        year = request.form['availability']
#        cursor = mysql.cursor()
#        insert_query = '''INSERT INTO books (titleID, title, author, genre, pubisher, year, availability) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
#        cursor.execute(insert_query, (titleID, title, author, genre, pubisher, year, availability))
#        mysql.commit()
#        cursor.close()
#     return render_template('admin_form.html')
# --------------------------------------------------------
# @app.route("/add", methods=['GET', 'POST']) #Add Student
# def add():
#   if request.method == 'POST':
#     name = request.form['name']
#     email = request.form['email']
#     print(name,email)
#     cur = mysql.cursor() #create a connection to the SQL instance
#     s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
#     app.logger.info(s)
#     cur.execute(s)
#     mysql.commit()
#   else:
#     return render_template('add.html')

#   return '{"Result":"Success"}'
  
# @app.route("/") #Default - Show Data
# def hello(): # Name of the method
#   cur = mysql.cursor() #create a connection to the SQL instance
#   cur.execute('''SELECT * FROM students''') # execute an SQL statment
#   rv = cur.fetchall() #Retreive all rows returend by the SQL statment
#   Results=[]
#   for row in rv: #Format the Output Results and add to return string
#     Result={}
#     Result['Name']=row[0].replace('\n',' ')
#     Result['Email']=row[1]
#     Result['ID']=row[2]
#     Results.append(Result)
#   response={'Results':Results, 'count':len(Results)}
#   ret=app.response_class(
#     response=json.dumps(response),
#     status=200,
#     mimetype='application/json'
#   )
#   return ret #Return the data in a string format


#Run the flask app at port 8080
if __name__ == "__main__":
  # app.run(debug=True,host='0.0.0.0',port='8080')
  app.run(debug=True,host='0.0.0.0',port='8080',ssl_context=('cert.pem', 'privkey.pem'))
