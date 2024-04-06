# Setup Virtual Env
python3 -m venv venv
# Activate Virtual Env
source venv/bin/activate
# Add venv folder into gitignore file

# precheck: pip3 list
pip3 install -r requirement.txt
# postcheck: pip3 list

# Run Server
python3 app.py