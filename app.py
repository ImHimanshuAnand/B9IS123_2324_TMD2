from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from flask_cors import CORS
import json

# MySQL Database Connection
mysql = mysql.connector.connect(user='web', password='webPass',
  host='127.0.0.1',
  database='library')

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

#Route for user signup
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       userType = request.form['userType']
       email = request.form['email']
       password = request.form['password']
       print(userType,email,password)
       cursor = mysql.cursor();
       insert_query= ''' INSERT INTO login (userType, email, password) VALUES('{}','{}','{}');'''.format(userType,email,password)
       app.logger.info(insert_query)
       cursor.execute(insert_query)
       mysql.commit()
    else:   
       return render_template('signup.html')
    # flash("Signup successfull! Please Login.", "success")
    # signup_alert = "Signup successfull! Please wait a moment."    
    # return render_template('signup.html', signup_alert=signup_alert)
    return '{"Result":"Success"}'

@app.route("/login")#URL leading to method
def login(): # Name of the method
 return render_template('login.html')

@app.route("/userreservation")#URL leading to method
def userreservation(): # Name of the method
 return render_template('user_form.html')

@app.route("/adminform")#URL leading to method
def adminform(): # Name of the method
 return render_template('admin_form.html')



@app.route("/add", methods=['GET', 'POST']) #Add Student
def add():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    print(name,email)
    cur = mysql.cursor() #create a connection to the SQL instance
    s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
    app.logger.info(s)
    cur.execute(s)
    mysql.commit()
  else:
    return render_template('add.html')

  return '{"Result":"Success"}'
  
@app.route("/") #Default - Show Data
def hello(): # Name of the method
  cur = mysql.cursor() #create a connection to the SQL instance
  cur.execute('''SELECT * FROM students''') # execute an SQL statment
  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
  Results=[]
  for row in rv: #Format the Output Results and add to return string
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret #Return the data in a string format


if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem')) #Run the flask app at port 8080