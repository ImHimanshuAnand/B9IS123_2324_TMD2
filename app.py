from flask import Flask, render_template, request, jsonify, flash
import mysql.connector
from flask_cors import CORS
import json

# MySQL Database Connection
mysql = mysql.connector.connect(user='web', password='webPass',
  host='localhost',
  database='Library1')

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
CORS(app)
# My SQL Instance configurations

@app.route("/")
def main():
  return "Hello, The app is started!"

books = [
    { 'description': 'salary', 'amount': 5000 }
]
@app.route('/book')
def get_books():
    return jsonify(books)
@app.route('/book', methods=['POST'])
def add_book():
    books.append(request.get_json())
    return '', 200

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

#Route for user signup
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       UserType = request.form['UserType']
       Email = request.form['Email']
       Password = request.form['Password']
       print(UserType,Email,Password)
       cursor = mysql.cursor();
       insert_query= ''' INSERT INTO Users (UserType, Email, Password) VALUES('{}','{}','{}');'''.format(UserType,Email,Password)
       app.logger.info(insert_query)
       cursor.execute(insert_query)
       mysql.commit()
       flash("Signup successfull! Please Login.", "success")
       signup_alert = "Signup successfull! Please wait a moment."    
       return render_template('signup.html', signup_alert=signup_alert)
    else:   
       return render_template('signup.html')
  

# @app.route("/login")#URL leading to method
# def login(): # Name of the method
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         cursor = mysql.cursor();
#         select_query = '''SELECT * FROM login WHERE email='{}' AND password='{}';'''
#         app.logger.info(select_query)
#         cursor.execute(select_query)
#         user = cursor.fetchone()
#         if user:
#           # User exists, redirect to login or some other page 

#     # return render_template('login.html')

@app.route("/userreservation")#URL leading to method
def userreservation(): # Name of the method
    if request.method == 'POST':
      room_type = request.form['room_type']
      check_in_date = request.form['room_type']
      check_out_date = request.form['check_out_date']
      return render_template('reservation_confirmation.html',room_type=room_type)
    else:
      return render_template('user_form.html') 

@app.route("/adminform")#URL leading to method
def adminform(): # Name of the method
    if request.method == 'POST':
       titleID = request.form['titleID']
       title = request.form['title']
       author = request.form['author']
       genre = request.form['genre']
       pulisher = request.form['year']
       year = request.form['availability']
       cursor = mysql.cursor()
       insert_query = '''INSERT INTO books (titleID, title, author, genre, pubisher, year, availability) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
       cursor.execute(insert_query, (titleID, title, author, genre, pubisher, year, availability))
       mysql.commit()
       cursor.close()
    return render_template('admin_form.html')

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
  app.run(host='0.0.0.0',port='8080',ssl_context=('cert.pem', 'privkey.pem'))
