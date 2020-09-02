from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


#Character creation form
class CCForm(FlaskForm):
    name = StringField("Character Name", validators=[InputRequired()])
    c_class = SelectField("Class", validators=[InputRequired()])
    race = SelectField("Race", validators=[InputRequired()])
    background = SelectField("Background", validators=[InputRequired()])
    equipment = SelectField("Equipment", validators=[InputRequired()])
    origin = SelectField("Place of Origin", validators=[InputRequired()])