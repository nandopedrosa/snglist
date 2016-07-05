"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.mail import Message
from flask import url_for
from app import app, mail
from app.decorators import async
from app.config import ADMINS


def send_confirmation(username, email, token):
    """
    Sends a confirmation email to a new user
    :param username: the name of the person who just registered
    :param email: the email of the recipient
    :param token: auth token
    :return: None
    """
    subject = get_text("Welcome to Songlist Plus!")
    msg = Message(subject, recipients=email)
    msg.body = get_text(
        """Dear {0},

        Welcome to Songlist Plus!

        To confirm your account, please click on the following link:

        {1}

        Sincerely,

        The Songlist Plus Team

        Note: this is an automatic message, there is no need to reply.
        """).format(username, url_for('confirmation', token=token, _external=True))
    __send_email_async(app, msg)


def send_contact(username, reply_to, text_body):
    """
    Sends a contact message to the given recipients
    :param username: the name of the person who sent the contact message
    :param reply_to: the email of the person who sent the contact message
    :param text_body: the message
    :return: None
    """
    subject = '[snglist] {0} has sent you a message'.format(username)
    msg = Message(subject, recipients=ADMINS)
    msg.body = "Name: " + username + "\nReply to: " + reply_to + "\nMessage:\n" + text_body
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
