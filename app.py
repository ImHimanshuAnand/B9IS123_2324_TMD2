from flask import Flask, render_template, request,redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
# from flask_bcrypt import Bcrypt
import mysql.connector
from flask_cors import CORS
import json
from books_routes import books_bp

# MySQL Database Connection
mysql = mysql.connector.connect(
  user='web', 
  password='webPass',
  host='localhost',
  database='LibraryManagementSystem'
)

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
app.register_blueprint(books_bp, url_prefix='/api')
app.secret_key = 'Library_Management_secret_key'
CORS(app)
# bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User class for Flask-Login 
class Users(UserMixin):
    def __init__(self,UserId,UserType,Email):
        self.id = UserId
        self.UserType = UserType
        self.Email =  Email

#Loader Function for Flask Login
@login_manager.user_loader
def load_user(UserId):
  user = query_user_by_id(UserId)
  if user:
    return user
  else:
    return None 

# Database query function to get user by ID 
def query_user_by_id(UserId):
     print(UserId)
     select_query = 'SELECT * FROM Users WHERE UserId = %s '
     cursor = mysql.cursor()
     cursor.execute(select_query,(UserId,))
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
  
@app.route("/books/list",methods=["GET"])
def book_list():
  return render_template("book_list.html")

@app.route("/books/add",methods=["GET"])
def book_add():
  return render_template("book_add.html")

# Route for user login
@app.route("/login" ,methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       UserType = request.form['UserType']
       Email = request.form['Email']
       Password = request.form['Password']
       cursor = mysql.cursor();
       select_query = '''SELECT * FROM Users WHERE Email='{}' AND Password='{}';'''.format(Email,Password)
       app.logger.info(select_query)
       cursor.execute(select_query)
       user = cursor.fetchone()
       if user:     
          session['UserID'] = user[0]
          session['UserType'] = user[1]
          session['Email'] = user[2]
          
          login_user(Users(user[0],user[1],user[2]))

          if session['UserType'] == 'Admin':
            return redirect(url_for('book_list'));
          else:
            return redirect(url_for('BookReservations'));
       else:
          return 'INVALID USERNAME OR PASSWORD'
    else:
      return render_template('login.html')

@app.route('/logout')
def logout():
  logout_user()
  session.pop('UserId', None)
  session.pop('UserType', None)
  session.pop('Email', None)
  return redirect(url_for('login'))

@app.route("/")
def defaultPage():
  return "Hello, Welcome to the Library"

@app.route("/BookReservations", methods=['Get','POST']) 
@login_required
def BookReservations(): 
  if current_user.UserType == "Student":
    if request.method == 'POST':
      try:
         UserName = request.form['UserName']
         Email = request.form['Email']
         UserPhone = request.form['UserPhone']
         BookTitle = request.form['BookTitle']
         IssueDate = request.form['IssueDate']
         ReturnDate = request.form['ReturnDate']
         cursor = mysql.cursor()
      
       # Check if the book is available before making a reservation
         check_book_query = "SELECT BookStatus, BookId FROM Books WHERE BookTitle = %s"
         cursor.execute(check_book_query, (BookTitle,))
         book_data = cursor.fetchone()

        if book_data and book_data[0] == "Available":
           insert_query='''INSERT INTO BookReservations (UserName, Email, UserPhone, BookTitle, IssueDate, ReturnDate,UserId,BookId) VALUES('{}','{}','{}','{}','{}','{}');'''.format (UserName, Email, UserPhone, BookTitle, IssueDate, ReturnDate, current_user.UserId,book_data[1])
           app.logger.info(insert_query)
           cursor.execute(insert_query)
           mysql.commit()
           return redirect(url_for('BookReservations'))
        else:
            return jsonify({'error': 'Book is not available for reservation'}), 400  
      except Exception as e:
         return jsonify({'error': str(e)}),500
    else:
       return render_template('user_form.html') 
  else:
    return "Unauthorized",403     
# --------------------------------------------------------------------------
# @app.route("/adminform", methods=['Get','POST'])
# @login_required
# def adminform(): 
#    if current_user.UserType == "Admin":
#       if request.method == 'POST':
#         try:
#            BookTitle = request.form['BookTitle']
#            BookAuthor = request.form['BookAuthor']
#            BookGenre = request.form['BookGenre']
#            BookPublisher = request.form['BookPublisher']
#            BookYear = request.form['BookYear']
#            cursor = mysql.cursor()
#            insert_query = '''INSERT INTO Admin (BookTitle, BookAuthor, BookGenre, BookPublisher, BookYear ) VALUES ('{}','{}','{}','{}','{}')'''.format (BookTitle, BookAuthor, BookGenre, BookPublisher, BookYear)
#            app.logger.info(insert_query)
#            cursor.execute(insert_query)
#            mysql.commit()
#            return redirect(url_for('adminform'))
#           #  return render_template('admin_form.html')
#         except Exception as e:
#            return jsonify({'error': str(e)}),500
#       else:
#        return render_template('admin_form.html') 
#    else:
#      return "Unauthorized",403       
         
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
