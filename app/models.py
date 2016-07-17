"""
models.py: Domain models


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, \
    AnonymousUserMixin  # Implements Login common functions (is_authenticated, is_active, etc.)
from flask.ext.login import AnonymousUserMixin
from flask import current_app


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    bands = db.relationship('Band', backref='user', lazy='dynamic')

    def __repr__(self):
        return 'User {0} ({1})'.format(self.name, self.email)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(128), nullable=False)
    style = db.Column(db.String(128))
    members = db.relationship('BandMember',
                              backref=db.backref('band'),
                              cascade="all, delete-orphan",
                              lazy='dynamic')

    def __repr__(self):
        return 'Band {0}'.format(self.name)


class BandMember(db.Model):
    __tablename__ = 'band_member'
    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return 'Band Member {0} ({1})'.format(self.name, self.email)
