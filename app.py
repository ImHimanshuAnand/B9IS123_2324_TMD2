from flask import Flask
from flask import render_template
from flask import request


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

app = Flask(__name__)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations

@app.route("/test", methods=['GET'])#URL leading to method
def test(): # Name of the method
   return render_template('login.html') #indent this line
#    return("Hello World!<BR/>THIS IS YET ANOTHER TEST!") 



if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080')
