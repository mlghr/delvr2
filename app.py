from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Character # Campaign
from forms import UserForm, CCForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///dnd_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template('home.html')

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
        redirect('/characters')

    return render_template('register.html', form=form)


@app.route('/characters/new', methods=['GET', 'POST'])
def new_character():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/')

    form = CCForm()

    if form.validate_on_submit():
        name = form.name.data
        c_class = form.c_class.data
        race = form.race.data
        background = form.background.data
        equipment = form.equipment.data
        new_chars = Character(name=name, c_class=c_class, race=race, background=background, equipment=equipment, user_id=session['user_id'])
        db.session.add(new_chars)
        print(f"here's {new_chars}")
        try:
            db.session.commit()
        except IntegrityError:
            form.name.errors.append('Username taken, choose another')
        return redirect('/characters')

    return render_template('new.html', form=form)

@app.route('/characters', methods=['GET'])
def show_characters():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/')

    characters = Character.query.all()
    return render_template('characters.html', characters=characters)

@app.route('/characters/<int:user_id>', methods=['POST'])
def delete_character(id):
    """Delete Character"""
    if 'user_id' not in session:
        flash('please login first!')
        return redirect('/characters')

    character = Character.query.get_or_404(id)
    if character.user_id == session['user_id']:
        db.session.delete(character)
        db.session.commit()
        flash("Character deleted!")
        return redirect('/characters')
    flash("Permission denied")
    return redirect('/characters')

@app.route('/characters/<int:user_id>', methods=['POST'])
def edit_character(id):
    """Edit Character"""
    if 'user_id' not in session:
        flash('please login first!')
        return redirect('/characters')

    character = Character.query.get_or_404(id)
    if character.user_id == session['user_id']:
        flash("Changes saved!")
        return redirect('/characters')
    flash("Permission denied")
    return redirect('/characters')