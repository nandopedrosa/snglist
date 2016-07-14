"""
util.py: Helper functions and constants

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.mail import Message
from flask import url_for
from flask.ext.babel import gettext
from app import app, mail
from app.decorators import async
from app.config import ADMINS
from flask.ext.login import current_user

# Constants
CONTACT_MAIL_BODY = "Name: {0} \n\nReply to: {1} \n\nMessage:\n\n{2}"

CONFIRMATION_MAIL_BODY = gettext("""Welcome to Songlist Plus!

To confirm your account, please click on the following link:

{1}

Sincerely,

The Songlist Plus Team

Note: this is an automatic message, there is no need to reply.
""")


def send_email(to, subject, body):
    """
    :param to: recipient of the email (could be a list)
    :param subject: the subject of the email
    :param body: the text body of the email
    :return: none
    """
    msg = Message(subject, recipients=to)
    msg.body = body
    __send_email_async(app, msg)


# noinspection PyShadowingNames
@async
def __send_email_async(app, msg):
    """
    Helper function to make send emails asynchronously (there' no point making the user wait for the email to be sent)
    :param app: the flask app
    :param msg: the msg object from Flask Mail
    :return: None
    """
    with app.app_context():
        mail.send(msg)


def is_current_user(user_id):
    """
    Checks if a given User Id is really the Current User
    :param user_id: a User id
    :return: True if user_id is the Current User, False otherwise
    """
    if current_user.id == user_id:
        return True
    else:
        return False
