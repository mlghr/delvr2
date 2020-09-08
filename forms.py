from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SelectField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


#Character creation form
class CCForm(FlaskForm):

    name = StringField("Character Name", validators=[InputRequired()])

    c_class = SelectField("Class", 
    choices=[("cleric", "Cleric"), ("druid", "Druid"), ("fighter", "Fighter")], 
    validators=[InputRequired()])

    race = SelectField("Race", 
    choices=[("dwarf", "Dwarf"), ("high-elf", "High-Elf"), ("human", "Human")], 
    validators=[InputRequired()])

    background = SelectField("Background", 
    choices=[("acolyte", "Acolyte"), ("noble", "Noble"), ("sailor", "Sailor")], 
    validators=[InputRequired()])

    equipment = SelectField("Equipment", 
    choices=[("standard", "Standard")], 
    validators=[InputRequired()])
    
    origin = SelectField("Place of Origin", 
    choices=[("place", "Cat"), ("dog", "Dog"), ("turtle", "Turtle")], 
    validators=[InputRequired()])

#class CampaignForm(FlaskForm):
#
#    title = StringField("Campaign Name", validators=[InputRequired()])





