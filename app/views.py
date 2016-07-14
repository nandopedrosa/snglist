"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from flask import render_template, request, session, redirect, url_for, jsonify, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.babel import gettext, lazy_gettext
from app import app, babel, db
from app.config import LANGUAGES
from app.forms import ContactForm, SignupForm, LoginForm, ProfileForm, BandForm
from app.util import send_email, CONTACT_MAIL_BODY, CONFIRMATION_MAIL_BODY, is_current_user
from app.models import User, Band


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page
    :return: The rendered index page
    """

    return render_template("home.html")


@app.route('/change-language', methods=['POST'])
def change_language():
    """
    Changes the language of the app for a given session
    :return: just a generic String (it is mandatory to return something in route functions)
    """

    if 'lang' in session:
        if 'en' == session['lang']:
            session['lang'] = 'pt'
        else:
            session['lang'] = 'en'
    else:
        session['lang'] = 'pt'

    return 'Changed language'


@babel.localeselector
def get_locale():
    """
    Gets the current language for the application
    :return: the current language
    """
    if 'lang' in session:
        return session['lang']
    else:
        'en'


@app.route('/contact', methods=["GET", "POST"])
def contact():
    """
    Sends a contact message
    :return:
    GET: The Contact Form page

    POST: a JSON file with status code (OK/ERROR). If an error occurs, the JSON file also has a list with the error
    messages and related fields
    """
    if request.method == 'GET':
        return render_template("contact.html", contact_form=ContactForm())

    form = ContactForm(request.form)

    if form.validate():
        form.errors['error'] = False
        body = CONTACT_MAIL_BODY.format(form.name.data, form.email.data, form.message.data)
        send_email([form.email.data], '[snglist] Someone has sent you a contact message', body)
        form.errors['msg'] = gettext('Message successfully sent')
    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Your message could not be sent. Check the errors below.')

    return jsonify(form.errors)


@app.route('/info')
def info():
    """
    Renders the More Info Page
    :return: The rendered "More Info" Page
    """
    return render_template("info.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Renders the signup page
    :return: The rendered contact page
    """
    if request.method == 'GET':
        return render_template("signup.html", signup_form=SignupForm())

    form = SignupForm(request.form)

    if form.validate():
        form.errors['error'] = False

        # We add the user to the Database with a pending confirmation
        user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # Then we send a confirmation email
        token = user.generate_confirmation_token()
        body = CONFIRMATION_MAIL_BODY.format(user.name, url_for('confirm', token=token, _external=True))
        send_email([user.email], gettext('Welcome to Songlist Plus!'), body)

        form.errors['msg'] = gettext(
            'Signup succesful. To complete your registration, check your email and follow the instructions.')

    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Signup unsuccessful. Check the errors below.')

    return jsonify(form.errors)


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    """
    Updates the user information
    :return: The rendered Profile page
    """

    if request.method == 'GET':
        form = ProfileForm()
        form.name.data = current_user.name
        return render_template("profile.html", profile_form=form)

    else:
        form = ProfileForm(request.form)

        if form.validate():
            form.errors['error'] = False

            # Update the user
            current_user.name = form.name.data

            if form.password.data and form.password.data != '':
                current_user.password = form.password.data

            db.session.add(current_user)

            form.errors['msg'] = gettext('Profile updated')

        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

        return jsonify(form.errors)


@app.route('/delete-user', methods=["POST"])
@login_required
def delete_user():
    """
    Deletes a user (logical deletion)
    :return: The home page
    """
    db.session.delete(current_user)
    flash(gettext('Your account has been deleted. Thanks for using Songlist Plus!'))
    return jsonify(dict())


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Confirms (activates) a user, given a valid token (the real implementation is in the Login function)
    :param token: the authentication token
    :return: the main page (with a possible success message)
    """
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders login page
    :return: The rendered login page or a success logged in user (redirect)
    """
    form = LoginForm()

    if request.method == 'GET':
        if request.args.get('next') and 'confirm' in request.args.get('next'):
            session['confirmurl'] = request.args.get('next')
        else:
            session['confirmurl'] = None
        return render_template("login.html", login_form=form)

    if form.validate():
        # First we try to instantiate a valid user with the given credentials
        user = User.query.filter_by(email=form.email.data).first()

        # If the user is valid, then the login is successful
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(gettext('Login successful'))

            # Confirm token after login
            if session['confirmurl']:
                token = session['confirmurl'][9:]
                if not current_user.confirmed and current_user.confirm_token(token):
                    flash(gettext('You have confirmed your account. Thanks!'))
                else:
                    flash(gettext('The confirmation link is invalid or has expired.'))

                form.errors['error'] = False
                form.errors['msg'] = ''
        # If not, then we return an error message
        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Invalid email or password')

    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Login unsuccessful. Check the errors below')

    return jsonify(form.errors)


@app.route('/logout')
@login_required
def logout():
    """
    Signs out the current user
    :return: The main page
    """
    logout_user()
    flash(gettext('You have been logged out.'))
    return redirect(url_for('index'))


@app.route('/edit-band', methods=['GET', 'POST'])
@login_required
def edit_band():
    """
    Add or Edit a band
    :param id: the band id
    :return: The updated band info
    """
    # TODO: check if the band belongs to the current user

    if request.method == 'GET':
        form = BandForm()
        band_id = request.args.get('id')

        # Edit Band
        if band_id is not None:
            band = Band.query.get(int(band_id))

            if not is_current_user(band.user_id):
                return render_template("not-authorized.html")

            form.bandid.data = band.id
            form.name.data = band.name
            form.style.data = band.style

        return render_template("edit-band.html", band_form=form)

    else:
        form = BandForm(request.form)

        if form.validate():
            form.errors['error'] = False

            if form.bandid.data == '':
                # New Band
                band = Band(name=form.name.data, style=form.style.data, user_id=current_user.id)
                db.session.add(band)
                form.errors['msg'] = gettext('You have added a new band/project!')
            else:
                # Edit band
                band = Band.query.get(int(form.bandid.data))
                band.name = form.name.data
                band.style = form.style.data
                db.session.add(band)
                form.errors['msg'] = gettext('Band/Project info updated!')

        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

        return jsonify(form.errors)
