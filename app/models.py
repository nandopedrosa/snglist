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
from app.util import getsoup


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    bands = db.relationship('Band', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    songs = db.relationship('Song', backref='user', lazy='dynamic', cascade="all, delete-orphan")

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


class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128))
    key = db.Column(db.String(128))
    tempo = db.Column(db.Integer)
    duration = db.Column(db.String(5))
    lyrics = db.Column(db.Text)
    notes = db.Column(db.String(4000))

    def __repr__(self):
        return self.title

    def pretty_duration(self):
        return self.duration[:2] + ':' + self.duration[2:]

    @staticmethod
    def get_lyrics_or_chords(url):
        """
        Scrapes the HTML of a given song Lyrics or Chords
        :param url: The url of the song (different Providers)
        :return: HTML of the song's Lyrics or Chords
        """
        html = ''

        if 'cifraclub' in url:
            if url.startswith('https://m.'):
                url = 'https://www.' + url[10:]  # So we don't have to deal with mobile URLs
            url += 'imprimir.html#columns=false'  # Printer Friendly page (it's cleaner)
            soup = getsoup(url)
            sections = soup.find_all('pre')
            for s in sections:
                html += str(s)

        if 'letras.mus.br' in url:
            if url.startswith('https://m.'):
                url = 'https://www.' + url[10:]  # So we don't have to deal with mobile URLs
            soup = getsoup(url)
            article = soup.find('article')
            html = str(article)

        if 'e-chords' in url:
            soup = getsoup(url)
            pre = soup.find('pre', id='core')
            # Remove Tab Div, keep raw tab
            div = pre.find('div')
            if div is not None:
                tab = div.find('div', class_='tab')
                html = '<pre>' + tab.text + '</pre>'
                div.extract()
            html += str(pre)

        if 'freak' in url:
            soup = getsoup(url)
            content = soup.find('div', id='content_h')
            html = str(content)

        return html
