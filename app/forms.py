"""
forms.py: Application forms

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.widgets import TextArea, TextInput
from wtforms.validators import InputRequired, Length, Email
from flask.ext.babel import lazy_gettext


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


# noinspection PyAbstractClass
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
