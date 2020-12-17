# Delvr 
is a DnD character creation application, made with Python3 and Flask as the framework and SQLAlchemy as the database ORM. 

![alt text](https://github.com/mlghr/delvr/blob/tablet/home-page.jpg?raw=true)
![alt text](https://github.com/mlghr/delvr/blob/tablet/home.jpg?raw=true)

# To use this application:
install postgresql
install python3

```
createdb dnd_db
pip install -r requirements.txt
psql -f seed.py
python -m venv venv
source venv/scripts/activate OR source venv/bin/activate (MacOS)
flask run
```
Navigate to http://127.0.0.1:5000 in your browser

Create an account and begin creating a character by filling out the character creation form. You may also create and view campaigns created by others using the application. At this time, joining campaigns via the app is not implemented.

API: https://open5e.com/api-docs