"""
forms.py: Application forms

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, HiddenField, IntegerField, ValidationError
from wtforms.widgets import TextArea, TextInput, PasswordInput, CheckboxInput, HiddenInput
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional, NumberRange
from flask.ext.babel import lazy_gettext
from flask.ext.login import current_user
from app.models import User


# Angular Models (necessary to render custom angular attributes)
class AngularJSTextInput(TextInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSTextInput, self).__call__(field, **kwargs)


class AngularJSHiddenInput(HiddenInput):
    def __call__(self, field, **kwargs):
        for key in list(kwargs):
            if key.startswith('ng_'):
                kwargs['ng-' + key[3:]] = kwargs.pop(key)
        return super(AngularJSHiddenInput, self).__call__(field, **kwargs)


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
                           Length(min=3, message=lazy_gettext("Your name must have a minimum of 3 characters")),
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
                           Length(min=3, message=lazy_gettext("Your name must have a minimum of 3 characters")),
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

    # noinspection PyMethodMayBeStatic
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email already registered.'))


class ProfileForm(Form):
    name = StringField(lazy_gettext("Name"), widget=AngularJSTextInput(), description=lazy_gettext('Enter your name'),
                       validators=[
                           InputRequired(lazy_gettext("Please, enter your name")),
                           Length(min=3, message=lazy_gettext("Your name must have a minimum of 3 characters")),
                           Length(max=128, message=lazy_gettext("Your name must have a maximum of 128 characters"))
                       ])

    password = PasswordField(lazy_gettext("New Password"),
                             widget=AngularJSPasswordInput(),
                             description=lazy_gettext('Enter your password (at least 6 characters)'),
                             validators=[Optional(),
                                         Length(min=6,
                                                message=lazy_gettext("Your password must have at least 6 characters")),
                                         EqualTo('password2', message=lazy_gettext('Passwords must match'))])

    password2 = PasswordField(lazy_gettext("Confirm New Password"),
                              widget=AngularJSPasswordInput(),
                              description=lazy_gettext('Confirm your password'))

    currentpassword = PasswordField(lazy_gettext("Please enter your current password to confirm changes:"),
                                    widget=AngularJSPasswordInput(),
                                    description=lazy_gettext('Enter your current password'),
                                    validators=[InputRequired(lazy_gettext("Please, enter your current password")),
                                                Length(min=6,
                                                       message=lazy_gettext(
                                                           "Your password must have at least 6 characters"))
                                                ])

    # noinspection PyMethodMayBeStatic
    def validate_currentpassword(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError(lazy_gettext('Invalid current password'))


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


class BandForm(Form):
    bandid = HiddenField(widget=AngularJSHiddenInput())

    name = StringField(lazy_gettext("Name"), widget=AngularJSTextInput(),
                       description=lazy_gettext('Enter your band/project name'),
                       validators=[
                           InputRequired(lazy_gettext("Please, enter your band/project name")),
                           Length(min=3,
                                  message=lazy_gettext("Your band/project name must have a minimum of 3 characters")),
                           Length(max=128,
                                  message=lazy_gettext("Your band/project name must have a maximum of 128 characters"))
                       ])

    style = StringField(lazy_gettext("Style"), widget=AngularJSTextInput(),
                        description=lazy_gettext('Enter the musical style of your band/project'),
                        validators=[
                            Length(min=3,
                                   message=lazy_gettext("Your band/project name must have a minimum of 3 characters")),
                            Length(max=128,
                                   message=lazy_gettext("Your band/project name must have a maximum of 128 characters"))
                        ])


class BandMemberForm(Form):
    bandid = HiddenField(widget=AngularJSHiddenInput())

    member_name = StringField(lazy_gettext("Name"), widget=AngularJSTextInput(),
                              description=lazy_gettext("Enter your bandmate's name"),
                              validators=[
                                  InputRequired(lazy_gettext("Please, enter your bandmate's name")),
                                  Length(max=128,
                                         message=lazy_gettext(
                                             "Your band/project name must have a maximum of 128 characters"))
                              ])

    member_email = StringField("Email", widget=AngularJSTextInput(),
                               description=lazy_gettext("Enter your bandmate's email"),
                               validators=[
                                   InputRequired(lazy_gettext("Please, enter your bandmate's email"))
                                   ,
                                   Length(min=6, message=lazy_gettext("The email must have a minimum of 6 characters"))
                                   , Email(message=lazy_gettext("Please, inform a valid email"))
                               ])


class SongForm(Form):
    songid = HiddenField(widget=AngularJSHiddenInput())

    title = StringField(lazy_gettext("Title"), widget=AngularJSTextInput(),
                        description=lazy_gettext("Enter the title of the song"),
                        validators=[
                            InputRequired(lazy_gettext("Please, enter the title of the song")),
                            Length(max=128,
                                   message=lazy_gettext(
                                       "The title of the song name must have a maximum of 128 characters"))
                        ])

    artist = StringField(lazy_gettext("Artist"), widget=AngularJSTextInput(),
                         description=lazy_gettext("Enter the name of the Band or Artist of the song"),
                         validators=[
                             Length(max=128,
                                    message=lazy_gettext(
                                        "The artist of the song name must have a maximum of 128 characters"))
                         ])

    key = StringField(lazy_gettext("Key"), widget=AngularJSTextInput(),
                      description=lazy_gettext("Key of the song (e.g: Am)"),
                      validators=[
                          Length(max=8,
                                 message=lazy_gettext(
                                     "The key of the song name must have a maximum of 128 characters"))
                      ])

    tempo = IntegerField('Tempo (bpm)', widget=AngularJSTextInput(),
                         description=lazy_gettext("Tempo of the song in beats per minute (e.g: 120)"),
                         validators=[Optional(),
                                     NumberRange(min=20, max=500,
                                                 message=lazy_gettext(
                                                     "Tempo must be between 20 and 500 bpm"))
                                     ])

    duration = StringField(lazy_gettext("Duration (mm:ss)"), widget=AngularJSTextInput(),
                           description=lazy_gettext("mm:ss"),
                           validators=[Optional(),
                               Length(min=4, max=4,
                                      message=lazy_gettext(
                                          "You must specify minutes and seconds (with left zero-padding, if necessary)"))
                           ])

    notes = TextAreaField(lazy_gettext("Notes"), widget=AngularJSTextArea(),
                          validators=[
                              Length(max=4000,
                                     message=lazy_gettext("Your note must have between 3 and 4000 characters"))],
                          description=lazy_gettext('Enter notes witih important observations'))

    lyrics = TextAreaField(lazy_gettext("Lyrics/Chords"), widget=AngularJSTextArea(),
                           description=lazy_gettext('Enter the lyrics and/or chords of the song'))
