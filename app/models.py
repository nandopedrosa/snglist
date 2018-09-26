"""
models.py: Domain models


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin  # implements commons authentication functions
from flask import current_app
from app.util import getsoup
from sqlalchemy.sql import text

# Many-to-Many auxiliary table of Songs and Shows
setlist = db.Table(
    'setlist',
    db.Column('show_id', db.Integer, db.ForeignKey('show.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('song_position', db.Integer)
)

# Many-to-Many auxiliary table of Bands and Songs
band_songs = db.Table('band_songs',
                      db.Column('band_id', db.Integer, db.ForeignKey('band.id'), nullable=False),
                      db.Column('song_id', db.Integer, db.ForeignKey('song.id'), nullable=False)
                      )


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    bands = db.relationship('Band', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    songs = db.relationship('Song', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    shows = db.relationship('Show', backref='user', lazy='dynamic', cascade="all, delete-orphan")

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
        if self.duration is not None and self.duration != '':
            return self.duration[:2] + ':' + self.duration[2:]
        else:
            return ''

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

    def get_list_of_associated_bands(self):
        formatted_output = ''

        associated_bands = self.query.get(self.id).bands.order_by(Band.name).all()

        for band in associated_bands:
            formatted_output = formatted_output + band.name + ', '

        if len(formatted_output) > 0:
            formatted_output = formatted_output[:-2]

        return formatted_output


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
    """
    Configuration for a many to many relationship between Shows and Songs

    1. 'Song' is the right side entity of the relationship (the left side entity is the parent class).
    2. secondary configures the association table that is used for this relationship. See auxiliary tables at the top
       of this file
    3. primaryjoin indicates the condition that links the left side entity  with the association table.
    4. secondaryjoin indicates the condition that links the right side entity with the association table.
    5. backref defines how this relationship will be accessed from the right side entity.
       The additional lazy argument indicates the execution mode for this query. A mode of dynamic sets up the query to
       not run until specifically requested.
    6. lazy is similar to the parameter of the same name in the backref, but this one applies to the left side query
       instead of the right side.
    """
    songs = db.relationship('Song',
                            secondary=band_songs,
                            primaryjoin=(band_songs.c.band_id == id),
                            secondaryjoin=(band_songs.c.song_id == Song.id),
                            backref=db.backref('bands', lazy='dynamic'),
                            lazy='dynamic')

    def associate_song(self, song):
        """
        Adds a song to the association list
        :param song: The song object to be added
        :return: None
        """
        self.songs.append(song)

    def disassociate_song(self, song):
        """
        Removes a song from the association list
        :param song: The song object to be removed
        :return: None
        """
        self.songs.remove(song)


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


# noinspection SqlDialectInspection
class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    name = db.Column(db.String(128), nullable=False)
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)
    address = db.Column(db.String(4000))
    contact = db.Column(db.String(4000))
    pay = db.Column(db.String(128))
    notes = db.Column(db.String(4000))

    """
    Configuration for a many to many relationship between Shows and Songs

    1. 'Song' is the right side entity of the relationship (the left side entity is the parent class).
    2. secondary configures the association table that is used for this relationship. See auxiliary tables at the top
       of this file
    3. primaryjoin indicates the condition that links the left side entity  with the association table.
    4. secondaryjoin indicates the condition that links the right side entity with the association table.
    5. backref defines how this relationship will be accessed from the right side entity.
       The additional lazy argument indicates the execution mode for this query. A mode of dynamic sets up the query to
       not run until specifically requested.
    6. lazy is similar to the parameter of the same name in the backref, but this one applies to the left side query
       instead of the right side.
    """
    songs = db.relationship('Song',
                            secondary=setlist,
                            order_by=setlist.c.song_position,
                            primaryjoin=(setlist.c.show_id == id),
                            secondaryjoin=(setlist.c.song_id == Song.id),
                            backref=db.backref('shows', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return self.name

    def add_song(self, song):
        """
        Adds a song to the show's setlist
        :param song: The song object to be added
        :return: None
        """
        self.songs.append(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def remove_all_songs(self):
        with db.engine.connect() as connection:
            delete_sql = text('delete from setlist where show_id = :show_id')
            delete_sql = delete_sql.bindparams(show_id=self.id)
            connection.execute(delete_sql.execution_options(autocommit=True))

    def assign_position(self, song, pos=None):
        """
        Assigns the correct order position for a new song added to the setlist
        :param song: the song to be ordered
        :param pos: the position, if it is known
        :return: None
        """
        if not pos:
            next_order = self.__get_max_pos() + 1
        else:
            next_order = pos

        update = text(
            "update setlist set song_position = :order where show_id = :show_id and song_id = :song_id")
        update = update.bindparams(order=next_order, show_id=self.id, song_id=song.id)

        db.engine.execute(update.execution_options(autocommit=True))

    def __get_max_pos(self):
        """
        Gets the position of the last song in the setlist
        :return: the position of the last song
        """
        query = text('select max(song_position) as "max_position" from setlist where show_id = :id')
        query = query.bindparams(id=self.id)

        result = db.engine.execute(query)

        for row in result:
            max_position = row['max_position']
            if max_position is None:
                max_position = 0

        result.close()

        return max_position
