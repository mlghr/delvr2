# Delvr 
is a DnD character creation application, made with Python3 and Flask as the framework and SQLAlchemy as the database ORM. 

![landing page](https://github.com/mlghr/delvr2/blob/main/home.jpg.png?raw=true)

![character info](https://github.com//mlghr/delvr2/blob/main/home-page.jpg.png?raw=true)


# Installation
install postgresql
install python3
make a venv folder and activate it inside project folder

```
createdb dnd_db
pip install -r requirements.txt
psql -f seed.py
python -m venv venv
source venv/scripts/activate OR source venv/bin/activate (MacOS)
flask run
```
Navigate to http://127.0.0.1:5000 in your browser

# What you can do with this app

Create an account and begin creating a character by filling out the character creation form. 
You may also create and view campaigns created by others using the application. 
At this time, joining campaigns via the app is not implemented.

API: https://api.open5e.com