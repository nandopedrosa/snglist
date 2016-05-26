"""
util.py: Helper functions and constants common to several News Source operations

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.mail import Message
from app import app, mail
from app.decorators import async
from app.config import ADMINS


def send_email(username, reply_to, text_body):
    """
    Sends an email to the given recipients
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
