# Module: B9IS123_2324_TMD2 - Programming for Information Systems
[Link to Google Docs Documentation](https://docs.google.com/document/d/1BP2CsbGHD83c0s7JLD4JdVjrfBDxQUFI13GMh-crQ54/edit?usp=sharing)
## Team Members Name, StudentID, Emails
1. Anusha Beeraiah Mariswamy - 20028528 - anushagowda1598@gmail.com
2. Gopika Kurumkulathil Vijayakumar - 20017757 - kvgopika3@gmail.com
3. Himanshu Jasraj Anand - 20020118 - hv7460@gmail.com
4. Rizwana Basheer Basha - 20031946 - rizwanabasheer067@gmail.com

LIBRARY MANAGEMENT SYSTEM




[Flask Project Article](https://realpython.com/flask-project/)

<!-- YT LINK: https://www.youtube.com/watch?v=GZbeL5AcTgw -->
<!-- macOS/Linux -->
<!-- You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs -->
<!-- python3 -m venv .venv -->
<!-- Windows -->
<!-- You may also use `py -3 -m venv .venv -->
<!-- python -m venv .venv -->
<!-- source  venv/bin/activate-->
<!-- pip list -->
<!-- pip freeze >> requirements.txt -->
<!-- pip install -r requirements.txt -->


Steps to Setup on Azure Cloud:
1. git clone <repo-name>
2. cd <repo-name>
3. .env.db
4. Create a virtual environment for the app:
   1. py -m venv .venv
   2. .venv\scripts\activate
5. Install the dependencies:
   1. pip install -r requirements.txt
6. # Run database migration
flask db upgrade
# Run the app at http://127.0.0.1:5000
flask run



# Steps for DB:
1. WEB APP: https://medium.com/@hangyulson1004/steps-to-integrate-mysql-with-flask-on-a-ubuntu-server-covers-subprocess-exited-with-error-a9a731f683b9
2. https://docs.rackspace.com/docs/create-and-edit-users-in-mysql?source=post_page-----a9a731f683b9--------------------------------
3. MYSQL create user and password: https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
4. DEPLOY: https://www.reddit.com/r/flask/comments/fkccgy/i_have_created_a_flask_app_how_do_i_deploy_it/
<!-- Installation -->
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql.service
<!-- Check if installed or not -->
sudo mysql









<!-- Code From Prof. Paul's Moodle Page, to setup mariaDB -->
sudo apt update
sudo  apt -y upgrade
sudo apt -y install python3-pip
pip3 install Flask
sudo apt -y install mariadb-server mariadb-client libmariadbclient-dev
pip3 install flask_cors mysql-connector-python


<!-- Git Commands -->
git log - To check commit history
git pull - To pull changes into current branch
git add - To add changes to staging
git commit - To commit changes to local repo
git push - To push changes to remote repo
