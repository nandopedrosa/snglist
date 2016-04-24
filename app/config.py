# -*- coding: utf8 -*-
"""
config.py: Application configurations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import os

# Security settings for WTForms
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

# Flask-mail settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('SNG_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'songlistplus@gmail.com'
ADMINS = ['fpedrosa@gmail.com']

# available languages
LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

BABEL_DEFAULT_LOCALE = 'en_US'

# Database Configuration
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost/snglist'  # Development Database
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # Heroku Database

SQLALCHEMY_TRACK_MODIFICATIONS = False
