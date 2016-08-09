# -*- coding: utf8 -*-
"""
config.py: Application configurations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))

# Security settings for WTForms
CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY')

# Flask-mail settings (With MailGun)
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')

MAIL_SERVER = os.environ.get('MAILGUN_SMTP_SERVER', 'smtp.gmail.com')
MAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', 465)
MAIL_USERNAME = os.environ.get('MAILGUN_SMTP_LOGIN', 'songlistplus@gmail.com')
MAIL_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', None)
if not MAIL_PASSWORD:
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

MAIL_DEFAULT_SENDER = 'songlistplus@gmail.com'

ADMINS = ['fpedrosa@gmail.com']


# BABEL
LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

BABEL_DEFAULT_LOCALE = 'en_US'

# Database Configuration
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(basedir, 'data.db') + '?check_same_thread=False')  # Development Database (SQLite)
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']  # Heroku Database

# SSL Handling
SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
