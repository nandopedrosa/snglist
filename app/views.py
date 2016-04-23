"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

import json
from flask import render_template, request, session, redirect, url_for, jsonify
from flask.ext.babel import gettext
from app import app, babel
from datetime import datetime
from app.config import LANGUAGES


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page
    :return: The rendered index page
    """
    return render_template("base.html")