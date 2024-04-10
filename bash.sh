Guideline:
1. a newline seperates two different topics
2. commands are highlighted using double quotes.

"mkdir flask-server"
"cd flask-server"
"touch server.py"

# Setup Virtual Env
# Windows- "python3 -m venv <path>"
"python3 -m venv venv"

# Activate Virtual Env
# Windows- ".\<env-name>\Scripts\activate"
"source venv/bin/activate"

# Add venv folder into gitignore file

# precheck: "pip3 list"
"pip3 install -r requirement.txt"
# postcheck: "pip3 list"

"pip3 install Flask"

# Run Server
# "python3 app.py"
"python3 server.py"