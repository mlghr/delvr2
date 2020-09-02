from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Character
from forms import UserForm
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
            return redirect('/tweets')
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
        flash('Welcome! Succesfully created your account!')
        redirect('/cc')

    return render_template('register.html', form=form)


@app.route('/cc')
def show_character():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect('/')

    form = TweetForm()
    all_tweets = Tweet.query.all()
    if form.validate_on_submit():
        text = form.text.data
        new_tweet = Tweet(text=text, user_id=session['user_id'])
    return render_template('tweets.html', form=form)

@app.route('/cc/<int_id>', methods=['POST'])
def delete_tweet(id):
    """Delete Character"""
    if 'user_id' not in session:
        flash('please login first!')
        return redirect('/cc')

    character = Character.query.get_or_404(id)
    if tweet.user_id == session['user_id']:
        db.session.delete(character)
        db.session.commit()
        flash("Tweet deleted!")
        return redirect('/cc')
    flash("Permission denied")
    return redirect('/cc')