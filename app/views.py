"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from flask import render_template, request, session, redirect, url_for, jsonify
from flask.ext.babel import gettext
from app import app, babel
from app.config import LANGUAGES
from app.forms import ContactForm


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page
    :return: The rendered index page
    """

    return render_template("home.html")


@app.route('/contact', methods=["GET"])
def contact():
    """
    Renders the contact page
    :return: The rendered contact page
    """
    return render_template("contact.html", contact_form=ContactForm())


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
