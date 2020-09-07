from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt() 


def connect_db(app):
    """CONNECT TO DB"""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username =  db.Column(db.Text, nullable=False, unique=True)

    password =  db.Column(db.Text, nullable=False, unique=True)

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed pwd & return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal utf 8 string

        hashed_utf8 = hashed.decode("utf8")

        #returns instance of user w/ username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """validate that user exists & password is correct

        return user if valid; else return false
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            #return user instance
            return u

        else: 
            return False

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.Text, nullable=False)
    c_class = db.Column(db.Text, nullable=False)
    race = db.Column(db.Text, nullable=False)
    background = db.Column(db.Text, nullable=False)
    equipment = db.Column(db.Text, nullable=False)
    origin = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))

    user = db.relationship('User', backref="characters")
    # campaign = db.relationship('Campaign', backref="characters")

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=(datetime.utcnow))
    char_enroll = db.Column(db.Integer, default=0)
