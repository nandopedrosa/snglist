"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from flask import render_template, request, session, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.babel import gettext
from app import app, babel
from app.config import LANGUAGES
from app.forms import ContactForm, SignupForm
from app.util import send_email, CONTACT_MAIL_BODY, CONFIRMATION_MAIL_BODY


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
        body = CONFIRMATION_MAIL_BODY.format(form.name.data, url_for('confirmation', token='123456', _external=True))
        send_email([form.email.data], 'Welcome to Songlist Plus!', body)
        form.errors['msg'] = gettext('Signup succesful')
    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Signup unsuccessful. Check the errors below.')

    return jsonify(form.errors)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Confirms (activates) a user, given a valid token
    :param token: the authentication token
    :return: the main page (with a possible success message)
    """
    None
