# Delvr 
is a DnD character creation application, made with Python3 and Flask as the framework and SQLAlchemy as the database ORM. 

![home](https://user-images.githubusercontent.com/64651384/104807218-230f9e80-5792-11eb-9b91-9d38160b83ed.png)
![character_view](https://user-images.githubusercontent.com/64651384/104807219-24d96200-5792-11eb-9eb7-527245754666.png)


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
