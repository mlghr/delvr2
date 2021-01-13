from flask import Flask, render_template, redirect, session, flash, request
import requests
from models import connect_db, db, User, Character, Campaign
from forms import UserForm, CharacterForm, CampaignForm
from sqlalchemy.exc import IntegrityError
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "postgres:///dnd_db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY',"secret1") #heroku issue?

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    
    return render_template('home.html')

# add timeout token expire to login

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.id

            return redirect('/characters')
        else: 
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    session['user_in_session'] = False
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register_user():

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)

        try :
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken, choose another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Account succesfully created')
        return redirect('/login')

    return render_template('register.html', form=form)


############## CHARACTER ROUTES

@app.route('/characters/new', methods=['GET', 'POST'])
def create_character():
    """Creates a new character"""
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/')

    form = CharacterForm()

    if form.validate_on_submit():
        name = form.name.data
        c_class = form.c_class.data
        race = form.race.data
        background = form.background.data
        equipment = form.equipment.data
        origin = form.origin.data

        character = Character(
        name=name, c_class=c_class, race=race, 
        background=background, equipment=equipment,
        origin=origin, user_id=session['user_id']
        )
        
        db.session.add(character)   
        db.session.commit()
        return redirect('/characters')

    return render_template('new_character.html', form=form)

@app.route('/characters')
def show_characters():
    """Displays all of a user's characters and allows for editing and deletion"""
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/login')

    characters = Character.query.all()
    baseURL = 'https://api.open5e.com'

    c_list = []
    r_list = []

    for character in characters:
        c = character.c_class
        r = character.race
        class_res = requests.get(f'{baseURL}/classes/{c}').json()
        race_res = requests.get(f'{baseURL}/races/{r}').json()
        c_list.append(class_res)
        r_list.append(race_res)

    class_res = requests.get(f'{baseURL}/classes/bard').json()
    race_res = requests.get(f'{baseURL}/races/dwarf').json()
    
    ### Character class-based response variables
    hit_dice = class_res["hit_dice"]
    c_name = class_res["name"]
    equipment = class_res["equipment"]

    ### Race-based response variables
    r_name = race_res["name"]
    r_description = race_res["desc"]
    age = race_res["age"]
    speed = race_res["speed"]["walk"]
    traits = race_res["traits"]

    return render_template('characters.html', 
                            characters=characters, 
                            c_name=c_name,
                            hit_dice=hit_dice,
                            equipment=equipment,
                            r_name=r_name,
                            r_description=r_description,
                            age=age,
                            speed=speed,
                            traits=traits
                            )

@app.route('/characters/<int:character_id>/edit', methods=['POST', 'GET'])
def edit_character(character_id):
    """Edits the details of a Character"""
    if 'user_id' not in session:
        flash('please login first!')
        return redirect('/login')

    character = Character.query.get_or_404(character_id)

    form = CharacterForm()

    if form.validate_on_submit():
        character.name = form.name.data
        character.c_class = form.c_class.data
        character.race = form.race.data
        character.background = form.background.data
        character.equipment = form.equipment.data
        character.origin = form.origin.data

        db.session.commit()
        return redirect("/characters")

    if character.user_id == session['user_id']:
        return render_template('character_edit.html', character=character, form=form)

@app.route('/characters/<int:character_id>/enroll', methods=['GET', 'POST'])
def enroll_character(character_id):
    """Enroll character in specific campaign"""
 
    character = Character.query.get_or_404(character_id)
    return render_template('campaign_view.html', campaign=campaign, characters=characters)


@app.route('/characters/<int:character_id>/delete', methods=['POST', 'GET'])
def delete_character(character_id):
    """Delete Character"""
    if "user_id" not in session:
        flash("Access unauthorized.", "danger")
        return redirect("/characters")

    c = Character.query.get(character_id)

    db.session.delete(c)
    db.session.commit()

    return redirect(f"/characters")


############# CAMPAIGN ROUTES

@app.route('/campaigns')
def show_campaigns():
    """Display all active campaigns for users to join"""
    if 'user_id'  not in session:
        flash('please login first!')
        return redirect('characters')

    campaigns = Campaign.query.all()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/campaigns/new', methods=['GET', 'POST'])
def create_campaign():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/login')

    form = CampaignForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        max_players = form.max_players.data
        
        campaign = Campaign(
        title=title, 
        description=description, 
        max_players=max_players, 
        user_id=session['user_id']
        )

        db.session.add(campaign)   
        db.session.commit()
        return redirect('/campaigns')
    
    return render_template('new_campaign.html', form=form)

@app.route('/campaigns/<int:campaign_id>/add-character/<int:character_id>', methods=['GET', 'POST'])
def add_character_to_campaign(character_id, campaign_id):
    """Adds one character to the campaign list and stores character in enrolled table"""
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/login')

    character = Character.query.get_or_404(character_id)

    if not character:
        flash('Character does not exist')


    data = Enrolled(character_id=character_id, campaign_id=campaign_id)

    db.session.add(data)
    db.session.commit()

    # if character not in campaign
    
    return render_template('campaign_character_add.html', campaign=campaign, character=character)


@app.route('/campaigns/<int:campaign_id>/details', methods=['GET', 'POST'])
def view_one_campaign(campaign_id):
    """Shows one campaign with details about players/characters"""
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/login')

    # add SQL join statement for all enrolled characters

    characters = Character.query.all()
    campaign = Campaign.query.get_or_404(campaign_id)

    return render_template('campaign_details.html', campaign=campaign, characters=characters)

@app.route('/campaigns/<int:campaign_id>/edit', methods=['POST'])
def edit_campaign(campaign_id):
    """Edit Campaign"""
    if 'user_id' not in session:
        flash('please login first!')
        return redirect('/login')

    campaign = Campaign.query.get_or_404(id)
    if campaign.user_id == session['user_id']:
        flash("Changes saved!")
        return redirect('/campaigns')

    flash("Permission denied")
    return redirect('/characters')

@app.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
def delete_campaign(campaign_id):
    """Delete Campaign"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/characters")

    campaign = Campaign.query.get(campaign_id)

    db.session.delete(campaign)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")



@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404