"""
forms.py: Application forms

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea, TextInput, PasswordInput, CheckboxInput
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask.ext.babel import lazy_gettext
from app.models import User


# Angular Models (necessary to render custom angular attributes)
class AngularJSTextInput(TextInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSTextInput, self).__call__(field, **kwargs)


class AngularJSTextArea(TextArea):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSTextArea, self).__call__(field, **kwargs)


class AngularJSPasswordInput(PasswordInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSPasswordInput, self).__call__(field, **kwargs)


class AngularJSCheckboxInput(CheckboxInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSCheckboxInput, self).__call__(field, **kwargs)


class ContactForm(Form):
    name = StringField(lazy_gettext("Name"), widget=AngularJSTextInput(), description=lazy_gettext('Enter your name'),
                       validators=[
                           InputRequired(lazy_gettext("Please, enter your name")),
                           Length(min=2, message=lazy_gettext("Your name must have a minimum of 3 characters")),
                           Length(max=128, message=lazy_gettext("Your name must have a maximum of 128 characters"))
                       ])

    email = StringField("Email", widget=AngularJSTextInput(), description=lazy_gettext('Enter your email'), validators=[
        InputRequired(lazy_gettext("Please, enter your email"))
        , Length(min=6, message=lazy_gettext("Your email must have a minimum of 6 characters"))
        , Email(message=lazy_gettext("Please, inform a valid email"))
    ])

    message = TextAreaField(lazy_gettext("Message"), widget=AngularJSTextArea(), validators=[
        InputRequired(lazy_gettext("Please, write your message"))
        , Length(min=3, max=4000, message=lazy_gettext("Your message must have between 3 and 4000 characters"))
    ], description=lazy_gettext(
        'Enter your message with suggestions, bug reports or anything else you think is important'))


class SignupForm(Form):
    name = StringField(lazy_gettext("Name"), widget=AngularJSTextInput(), description=lazy_gettext('Enter your name'),
                       validators=[
                           InputRequired(lazy_gettext("Please, enter your name")),
                           Length(min=2, message=lazy_gettext("Your name must have a minimum of 3 characters")),
                           Length(max=128, message=lazy_gettext("Your name must have a maximum of 128 characters"))
                       ])

    email = StringField("Email", widget=AngularJSTextInput(), description=lazy_gettext('Enter your email'), validators=[
        InputRequired(lazy_gettext("Please, enter your email"))
        , Length(min=6, message=lazy_gettext("Your email must have a minimum of 6 characters"))
        , Email(message=lazy_gettext('Please, inform a valid email'))
    ])

    password = PasswordField(lazy_gettext("Password"),
                             widget=AngularJSPasswordInput(),
                             description=lazy_gettext('Enter your password (at least 6 characters)'),
                             validators=[
                                 InputRequired(lazy_gettext('Please, enter your password')),
                                 Length(min=6, message=lazy_gettext("Your password must have at least 6 characters")),
                                 EqualTo('password2', message=lazy_gettext('Passwords must match'))])

    password2 = PasswordField(lazy_gettext("Confirm Password"),
                              widget=AngularJSPasswordInput(),
                              description=lazy_gettext('Confirm your password'),
                              validators=[InputRequired(lazy_gettext('Please, confirm your password'))])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email already registered.'))


class LoginForm(Form):
    email = StringField("Email", widget=AngularJSTextInput(), description=lazy_gettext('Enter your email'), validators=[
        InputRequired(lazy_gettext("Please, enter your email"))
        , Length(min=6, message=lazy_gettext("Your email must have a minimum of 6 characters"))
        , Email(message=lazy_gettext("Please, inform a valid email"))
    ])

    password = PasswordField(lazy_gettext("Password"),
                             widget=AngularJSPasswordInput(),
                             description=lazy_gettext('Enter your password (at least 6 characters)'),
                             validators=[
                                 InputRequired(lazy_gettext('Please, enter your password')),
                                 Length(min=6, message=lazy_gettext("Your password must have at least 6 characters")),
                             ])

    remember_me = BooleanField(lazy_gettext('Keep me logged in'),
                               widget=AngularJSCheckboxInput())
