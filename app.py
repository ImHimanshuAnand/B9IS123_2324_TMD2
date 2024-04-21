from flask import Flask, render_template, request,redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
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

# Route for HomePage
@app.route("/")
def defaultPage():
  return render_template('home.html')

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
            return redirect(url_for('reservation'));
       else:
          return 'INVALID USERNAME OR PASSWORD'
    else:
      return render_template('login.html')

# Route for Admin_Dashboard 
@app.route("/books/list",methods=["GET"])
@login_required
def book_list():
  if current_user.UserType == "Admin":
    return render_template("book_list.html")
  else:
    return "Unauthorized",403   
# Admin Add feature
@app.route("/books/add",methods=["GET"])
def book_add():
  return render_template("book_add.html")
# Admin Edit Feature 
@app.route("/books/edit/<int:bookId>",methods=["GET"])
def book_edit(bookId):
  return render_template("book_edit.html",bookId=bookId)

# Route for User_Dashboard 
@app.route("/reservation",methods=["GET"])
@login_required
def reservation():
  if current_user.UserType == "Student":
    return render_template("User_dashboard.html")
  else:
    return "Unauthorized",403


# Route for User BookReservation
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

         if book_data and book_data[0] == "Available" :
           insert_query='''INSERT INTO BookReservations (UserName, Email, UserPhone, BookTitle, IssueDate, ReturnDate,UserId,BookId) VALUES('{}','{}','{}','{}','{}','{}',(SELECT UserId FROM Users WHERE Email= '{}'),'{}');'''.format (UserName, Email, UserPhone, BookTitle, IssueDate, ReturnDate, Email,book_data[1])
           app.logger.info(insert_query)
           cursor.execute(insert_query)
           mysql.commit()

           flash("Book is Reserved successfull!", "success")
           alert = "Reservation successfull!" 
           return redirect(url_for('reservation'))
         else:
            return jsonify({'error': 'Book is not available for reservation'}), 400  
      except Exception as e:
         return jsonify({'error': str(e)}),500
    else:
       return render_template('user_form.html') 
  else:
    return "Unauthorized",403  

# Route for Logout
@app.route('/logout')
def logout():
  logout_user()
  session.pop('UserId', None)
  session.pop('UserType', None)
  session.pop('Email', None)
  return redirect(url_for('login'))     

#Run the flask app at port 8080
if __name__ == "__main__":
  # app.run(debug=True,host='0.0.0.0',port='8080')
  app.run(debug=True,host='0.0.0.0',port='8080',ssl_context=('cert.pem', 'privkey.pem'))
