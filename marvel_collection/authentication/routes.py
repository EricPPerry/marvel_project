from flask import Blueprint, render_template, request, flash, redirect, url_for
from marvel_collection.forms import UserLoginForm, EditProfileForm, SignUpForm
from marvel_collection.models import User, db, check_password_hash, Character
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__, template_folder='auth_templates')

#added route to allow user to edit their profile, adding information/writing an 'about me' section if they choose to.
@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated.','user-edited')
        return redirect(url_for('auth.mycollection'))
    #in case the form does not validate correctly, resets fields to default/beginning values
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form = form)


@auth.route('/mycollection')
@login_required
def mycollection():
    #user_collection = Character.query.filter(Character.user_token == current_user.token).all()
    
    #owner = current_user.token user_token = f'{owner}'
    query_collection = Character.query.with_entities(Character.character_name, Character.user_token).all()
    user_collection = []
    for char, token in query_collection:
        if token == current_user.token:
            user_collection.append(char)
    return render_template('mycollection.html', user_collection = user_collection)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form= SignUpForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data

            #implementing this to keep track of outputs/help with potential error solving
            print(email, password, first_name, last_name, username)

            user = User(email, password = password, first_name = first_name, last_name = last_name, username = username)

            db.session.add(user)
            db.session.commit()
            flash(f'You have successfully created a user account:{username}! Welcome, please login to start your new collection!', 'user-created')

            return redirect(url_for('main_site.home'))
    
    except:
        raise Exception('Sorry, Invalid Form Data: Please check your form inputs.')
    return render_template('signup.html', form = form)

@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in via: email/password', 'auth-success')
                return redirect(url_for('main_site.home'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please check your form!')
    
    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_site.home'))