from flask import Flask
app = Flask(__name__)
@app.route("/")#URL leading to method
def hello(): # Name of the method
 return("Hello World!") #indent this line
if __name__ == "__main__":
<<<<<<< HEAD
 # app.run(host='0.0.0.0',port='8080') # indent this line 
    app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem')) #Run the flask app at port 8080
=======
   # app.run(host='0.0.0.0',port='8080')  # indent this line
   app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem')) #Run the flask app at port 8080
>>>>>>> 6a1ebc713c520297f044667caac4cdebdf1df8a3
