from app import db
from models import User, Character, Campaign


db.drop_all()
db.create_all()
