"""
views.py: Routing and view rendering of the application


__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask import render_template, request, session, redirect, url_for, jsonify, flash, make_response
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.babel import gettext, lazy_gettext, format_datetime
from json import loads
from app import app, babel, db
from app.config import LANGUAGES, ADMINS
from sqlalchemy import desc
from app.forms import ContactForm, SignupForm, LoginForm, ProfileForm, BandForm, BandMemberForm, SongForm, ShowForm
from app.util import send_email, CONTACT_MAIL_BODY, CONFIRMATION_MAIL_BODY, is_current_user, get_date_format, \
    create_pdf, allowed_file
from app.models import User, Band, BandMember, Song, Show


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    """
    Renders the index (home) page
    :return: The rendered index page
    """

    return render_template("home.html")


# noinspection PyUnusedLocal
@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html")


# noinspection PyUnusedLocal
@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html")


@app.route('/change-language', methods=['POST'])
def change_language():
    """
    Changes the language of the app for a given session
    :return: just a generic String (it is mandatory to return something in route functions)
    """

    if 'lang' in session:
        if 'en' == session['lang']:
            session['lang'] = 'pt'
        else:
            session['lang'] = 'en'
    else:
        session['lang'] = 'pt'

    return session['lang']


@babel.localeselector
def get_locale():
    """
    Gets the current language for the application
    :return: the current language
    """
    if 'lang' in session:
        return session['lang']
    else:
        'en'


@app.route('/contact', methods=["GET", "POST"])
def contact():
    """
    Sends a contact message
    :return:
    GET: The Contact Form page

    POST: a JSON file with status code (OK/ERROR). If an error occurs, the JSON file also has a list with the error
    messages and related fields
    """
    if request.method == 'GET':
        return render_template("contact.html", contact_form=ContactForm())

    form = ContactForm(request.form)

    if form.validate():
        form.errors['error'] = False
        body = CONTACT_MAIL_BODY.format(form.name.data, form.email.data, form.message.data)
        send_email(ADMINS, '[snglist] Someone has sent you a contact message', body)
        form.errors['msg'] = gettext('Message successfully sent')
    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Your message could not be sent. Check the errors below.')

    return jsonify(form.errors)


@app.route('/info')
def info():
    """
    Renders the More Info Page
    :return: The rendered "More Info" Page
    """
    return render_template("info.html")


# --------------------------------------  Users, Auth, Token, Profile ---------------------------------------

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Renders the signup page
    :return: The rendered contact page
    """
    if request.method == 'GET':
        return render_template("signup.html", signup_form=SignupForm())

    form = SignupForm(request.form)

    if form.validate():
        form.errors['error'] = False

        # We add the user to the Database with a pending confirmation
        user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # Then we send a confirmation email
        token = user.generate_confirmation_token()
        body = CONFIRMATION_MAIL_BODY.format(user.name, url_for('confirm', token=token, _external=True))
        send_email([user.email], gettext('Welcome to Songlist Plus!'), body)

        form.errors['msg'] = gettext(
            'Signup succesful. To complete your registration, check your email and follow the instructions.')

    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Signup unsuccessful. Check the errors below.')

    return jsonify(form.errors)


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    """
    Updates the user information
    :return: The rendered Profile page
    """

    if request.method == 'GET':
        form = ProfileForm()
        form.name.data = current_user.name
        return render_template("profile.html", profile_form=form)

    else:
        form = ProfileForm(request.form)

        if form.validate():
            form.errors['error'] = False

            # Update the user
            current_user.name = form.name.data

            if form.password.data and form.password.data != '':
                current_user.password = form.password.data

            db.session.add(current_user)

            form.errors['msg'] = gettext('Profile updated')

        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

        return jsonify(form.errors)


@app.route('/delete-user', methods=["POST"])
@login_required
def delete_user():
    """
    Deletes a user (logical deletion)
    :return: The home page
    """
    db.session.delete(current_user)
    flash(gettext('Your account has been deleted. Thanks for using Songlist Plus!'))
    return jsonify(dict())


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    Confirms (activates) a user, given a valid token (the real implementation is in the Login function)
    :param token: the authentication token
    :return: the main page (with a possible success message)
    """
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders login page
    :return: The rendered login page or a success logged in user (redirect)
    """
    form = LoginForm()

    if request.method == 'GET':
        if request.args.get('next') and 'confirm' in request.args.get('next'):
            session['confirmurl'] = request.args.get('next')
        else:
            session['confirmurl'] = None
        return render_template("login.html", login_form=form)

    if form.validate():
        # First we try to instantiate a valid user with the given credentials
        user = User.query.filter_by(email=form.email.data).first()

        # If the user is valid, then the login is successful
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(gettext('Login successful'))

            # Confirm token after login
            if session['confirmurl']:
                token = session['confirmurl'][9:]
                if not current_user.confirmed and current_user.confirm_token(token):
                    flash(gettext('You have confirmed your account. Thanks!'))
                else:
                    flash(gettext('The confirmation link is invalid or has expired.'))

            form.errors['error'] = False
            form.errors['msg'] = ''

            # If not, then we return an error message
        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Invalid email or password')

    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Login unsuccessful. Check the errors below')

    return jsonify(form.errors)


@app.route('/logout')
@login_required
def logout():
    """
    Signs out the current user
    :return: The main page
    """
    logout_user()
    flash(gettext('You have been logged out.'))
    return redirect(url_for('index'))


# --------------------------------------  End Users, Auth, Token, Profile --------------------------------


# --------------------------------------  Bands and Band Members -----------------------------------------

@app.route('/edit-band', methods=['GET', 'POST'])
@login_required
def edit_band():
    """
    Add or Edit a band
    :return: The updated band info
    """

    if request.method == 'GET':
        form = BandForm()
        member_form = BandMemberForm()
        band_id = request.args.get('id')

        # Edit Band
        if band_id is not None:
            band = Band.query.get(int(band_id))

            if not is_current_user(band.user_id):
                return render_template("not-authorized.html")

            form.bandid.data = band.id
            member_form.bandid.data = band.id
            form.name.data = band.name
            form.style.data = band.style

        return render_template("edit-band.html", band_form=form, member_form=member_form)

    else:
        form = BandForm(request.form)

        if form.validate():
            form.errors['error'] = False

            if form.bandid.data == '':
                # New Band
                band = Band(name=form.name.data, style=form.style.data, user_id=current_user.id)
                db.session.add(band)
                db.session.commit()
                form.errors['msg'] = gettext('You have added a new band/project!')
                form.errors['addedid'] = band.id
            else:
                # Edit band
                band = Band.query.get(int(form.bandid.data))
                band.name = form.name.data
                band.style = form.style.data
                db.session.add(band)
                form.errors['msg'] = gettext('Band/Project info updated!')

        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

        return jsonify(form.errors)


@app.route('/add-member', methods=['POST'])
@login_required
def add_member():
    """
    Adds a member to a band
    :return: JSON with messages and possible errors
    """
    form = BandMemberForm()

    if form.validate():
        form.errors['error'] = False
        member = BandMember(name=form.member_name.data, email=form.member_email.data, band_id=form.bandid.data)
        db.session.add(member)
        db.session.commit()
        form.errors['memberid'] = member.id
        form.errors['msg'] = gettext('Band member added')

    else:
        form.errors['error'] = True
        form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

    return jsonify(form.errors)


@app.route('/fetch-members/<int:band_id>', methods=['GET'])
@login_required
def fetch_members(band_id):
    """
    Fetches all the band members of a given band
    :param band_id: The id of the band
    :return: JSON with the band members
    """
    band = Band.query.get(band_id)
    members = band.members.order_by(BandMember.name).all()
    return_data = []

    for member in members:
        return_data.append(dict(name=member.name, email=member.email, id=member.id))

    return jsonify(data=return_data)


@app.route('/delete-member', methods=["POST"])
@login_required
def delete_member():
    """
    Deletes a band member
    :return: Empty Dict
    """
    member = BandMember.query.get(int(request.form.get('id')))
    db.session.delete(member)
    return jsonify(dict())


@app.route('/bands')
@login_required
def bands():
    """
    Renders the Bands Page
    :return: The rendered Bands Page
    """
    return render_template("bands.html")


@app.route('/fetch-bands/', methods=['GET'])
@login_required
def fetch_bands():
    """
    Fetch all the bands of the current user
    :return: JSON with the bands list
    """
    band_list = current_user.bands.order_by(Band.name).all()
    return_data = []

    for band in band_list:
        members = band.members.order_by(BandMember.name).all()
        members_str = ''  # Concatenated list of members (string representation, comma separated)

        for member in members:
            members_str = members_str + member.name + ', '

        members_str = members_str.strip()

        if members_str.endswith(','):
            members_str = members_str[:-1]

        return_data.append(dict(id=band.id, name=band.name, style=band.style, members=members_str))

    return jsonify(data=return_data)


@app.route('/delete-band', methods=["POST"])
@login_required
def delete_band():
    """
    Deletes a band and all its members
    :return: Empty Dict
    """
    band = Band.query.get(int(request.form.get('id')))
    db.session.delete(band)
    return jsonify(dict(msg=gettext('Band successfully deleted.')))


# --------------------------------------  End Bands and Band Members -----------------------------------------

# --------------------------------------  Songs --------------------------------------------------------------

@app.route('/edit-song', methods=['GET', 'POST'])
@login_required
def edit_song():
    """
    Add or Edit a song
    :return: The updated song info
    """

    if request.method == 'GET':
        form = SongForm()
        songid = request.args.get('id')

        # Edit Song
        if songid is not None:
            song = Song.query.get(int(songid))

            if not is_current_user(song.user_id):
                return render_template("not-authorized.html")

            form.songid.data = song.id
            form.title.data = song.title
            form.artist.data = song.artist
            form.key.data = song.key
            form.tempo.data = song.tempo
            form.duration.data = song.duration
            form.notes.data = song.notes
            form.lyrics.data = song.lyrics

        return render_template("edit-song.html", song_form=form)

    else:
        form = SongForm(request.form)

        if form.validate():
            form.errors['error'] = False

            if form.songid.data == '':
                # New Song
                song = Song(title=form.title.data, artist=form.artist.data, key=form.key.data, tempo=form.tempo.data,
                            duration=form.duration.data, notes=form.notes.data, lyrics=form.lyrics.data,
                            user_id=current_user.id)
                db.session.add(song)
                form.errors['msg'] = gettext(
                    'Song successfully added! Now you can associate your bands with this song. This is useful for filtering which songs belong to which of your bands.')
            else:
                # Edit Song
                song = Song.query.get(int(form.songid.data))
                song.title = form.title.data
                song.artist = form.artist.data
                song.key = form.key.data
                song.tempo = form.tempo.data
                song.duration = form.duration.data
                song.notes = form.notes.data
                song.lyrics = form.lyrics.data
                db.session.add(song)
                form.errors['msg'] = gettext('Song info updated!')

        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

        return jsonify(form.errors)


@app.route('/fetch-available-bands/<int:song_id>', methods=['GET'])
@login_required
def fetch_available_bands(song_id):
    """
    Fetch all the available bands from a given user that can be associated to a song
    :param song_id: the song to which associate a band
    :return: JSON with the bands list
    """
    song = Song.query.get(int(song_id))

    if not is_current_user(song.user_id):
        return render_template("not-authorized.html")

    available_bands = current_user.bands.order_by(Band.name).all()
    bands_associated_to_the_song = song.bands

    # Now we remove bands already associated to the song, and return only the leftover bands
    for associated_band in bands_associated_to_the_song:
        for band in available_bands:
            if associated_band.id == band.id:
                available_bands.remove(band)

    return_data = []

    for band in available_bands:
        return_data.append(dict(id=band.id, name=band.name))

    return jsonify(data=return_data)


@app.route('/fetch-associated-bands/<int:song_id>', methods=['GET'])
@login_required
def fetch_associated_bands(song_id):
    """
    Fetch all the bands associated to a song
    :param song_id: the song to which associate a band
    :return: JSON with the bands list
    """
    song = Song.query.get(int(song_id))

    if not is_current_user(song.user_id):
        return render_template("not-authorized.html")

    associated_bands = song.bands

    return_data = []

    for band in associated_bands:
        return_data.append(dict(id=band.id, name=band.name))

    return jsonify(data=return_data)


@app.route('/associate-band', methods=["POST"])
@login_required
def associate_band():
    """
    Associates a band with a song
    :return: the band just added
    """
    song = Song.query.get(int(request.form.get('songid')))
    band = Band.query.get(int(request.form.get('bandid')))

    band.associate_song(song)

    db.session.add(band)
    db.session.commit()
    return jsonify(dict(id=band.id, name=band.name))


@app.route('/disassociate-band', methods=["POST"])
@login_required
def disassociate_band():
    song = Song.query.get(int(request.form.get('songid')))
    band = Band.query.get(int(request.form.get('bandid')))

    band.disassociate_song(song)
    return jsonify(dict(id=band.id, name=band.name))


@app.route('/fetch-songs/', methods=['GET'])
@login_required
def fetch_songs():
    """
    Fetch all the songs of the current user
    :param band_id: -1 if you want all songs, or a given ID if you want to filter the songs associated with a specific band
    :return: JSON with the songs list
    """
    return_data = []

    song_list = current_user.songs.order_by(Song.title).all()

    for song in song_list:
        return_data.append(dict(id=song.id, title=song.title, artist=song.artist, tempo=song.tempo, key=song.key,
                                duration=song.pretty_duration(), lyrics=song.lyrics, bands=song.get_list_of_associated_bands()))

    return jsonify(data=return_data)


@app.route('/fetch-songs-by-band/<band_id>', methods=['GET'])
@login_required
def fetch_songs_by_band(band_id):
    """
    Fetch all the songs of the current user
    :param band_id: String 'null' if you want all songs, or a given ID if you want to filter the songs associated with a specific band
    :return: JSON with the songs list
    """
    return_data = []

    if band_id == 'null':
        song_list = current_user.songs.order_by(Song.title).all()
    else:
        song_list =  Band.query.get(int(band_id)).songs.order_by(Song.title).all()

    for song in song_list:
        return_data.append(dict(id=song.id, title=song.title, artist=song.artist, tempo=song.tempo, key=song.key,
                                duration=song.pretty_duration(), lyrics=song.lyrics, bands=song.get_list_of_associated_bands()))

    return jsonify(data=return_data)


@app.route('/songs')
@login_required
def songs():
    """
    Renders the Songs Page
    :return: The rendered Bands Page
    """
    return render_template("songs.html")


@app.route('/delete-song', methods=["POST"])
@login_required
def delete_song():
    """
    Deletes a song
    :return: Info message
    """
    song = Song.query.get(int(request.form.get('id')))
    db.session.delete(song)
    return jsonify(dict(msg=gettext('Song successfully deleted.')))


@app.route('/import-song', methods=["POST"])
@login_required
def import_song():
    """
    Imports a song lyrics or chords
    :return: JSON with html content or errors
    """
    url = request.form.get('url')

    if url is None or url == '':
        return jsonify(dict(error=gettext('You must provide a URL address')))

    html = Song.get_lyrics_or_chords(url)

    if html != '':
        return jsonify(dict(html=html, success=gettext('Song successfully imported. You can now close this dialog.')))
    else:
        return jsonify(
            dict(error=gettext(
                'We could not find the song you requested. Are you sure you entered a supported site URL?')))


# --------------------------------------  Shows --------------------------------------------------------------

@app.route('/edit-show', methods=['GET', 'POST'])
@login_required
def edit_show():
    """
    Add or Edit a show
    :return: The updated song info
    """

    if request.method == 'GET':
        form = ShowForm()
        showid = request.args.get('id')

        # Edit Song
        if showid is not None:
            show = Show.query.get(int(showid))

            if not is_current_user(show.user_id):
                return render_template("not-authorized.html")

            form.showid.data = show.id
            form.bandid.data = show.band_id
            form.name.data = show.name
            form.start.data = show.start
            form.end.data = show.end
            form.address.data = show.address
            form.contact.data = show.contact
            form.pay.data = show.pay
            form.notes.data = show.notes

        return render_template("edit-show.html", show_form=form)

    else:
        form = ShowForm(request.form)
        form.start.format = '%d/%m/%Y %H:%M'

        if form.validate():
            form.errors['error'] = False

            if form.showid.data == '':
                # New Show
                show = Show(name=form.name.data, start=form.start.data, end=form.end.data, contact=form.contact.data,
                            pay=form.pay.data, notes=form.notes.data, address=form.address.data,
                            band_id=form.bandid.data, user_id=current_user.id)
                db.session.add(show)
                db.session.commit()
                form.errors['msg'] = gettext(
                    'Show successfully added! Now you can start building your setlist (see below).')
                form.errors['addedid'] = show.id
            else:
                # Edit Show
                show = Show.query.get(int(form.showid.data))
                show.band_id = form.bandid.data
                show.name = form.name.data
                show.start = form.start.data
                show.end = form.end.data
                show.address = form.address.data
                show.contact = form.contact.data
                show.pay = form.pay.data
                show.notes = form.notes.data
                db.session.add(show)
                form.errors['msg'] = gettext('Show info updated!')

        else:
            form.errors['error'] = True
            form.errors['msg'] = gettext('Your request was not successful. Please, check the errors below.')

        return jsonify(form.errors)


@app.route('/fetch-shows/', methods=['GET'])
@login_required
def fetch_shows():
    """
    Fetch all the shows of the current user (from new to old)
    :return: JSON with the shows list
    """
    show_list = current_user.shows.order_by(desc(Show.start)).all()
    return_data = []

    for show in show_list:
        band = Band.query.get(int(show.band_id))
        if show.start:
            start = format_datetime(show.start, get_date_format())
        else:
            start = ''
        return_data.append(dict(id=show.id, name=show.name, start=start, band=band.name))

    return jsonify(data=return_data)


@app.route('/shows')
@login_required
def shows():
    """
    Renders the Shows Page
    :return: The rendered Shows Page
    """
    return render_template("shows.html")


@app.route('/formats/')
@login_required
def formats():
    """
    Returns the available file formats for sharing setlists
    :return: The file formats
    """
    # noinspection PyListCreation
    return_data = []
    return_data.append(dict(id=1, name=lazy_gettext('TXT (Titles Only)')))
    return_data.append(dict(id=2, name=lazy_gettext('PDF')))

    return jsonify(data=return_data)


@app.route('/recipients/<int:show_id>')
@login_required
def recipients(show_id):
    """
    Returns the available recipient options for sharing setlists
    :return: The recipient options
    """
    # noinspection PyListCreation
    return_data = []
    return_data.append(dict(id=1, name=lazy_gettext('Myself'), email=current_user.email))

    show = current_user.shows.filter_by(id=show_id).first()
    band = Band.query.get(int(show.band_id))
    members = band.members.order_by(BandMember.name).all()

    email = current_user.email

    for member in members:
        email = email + ', ' + member.email

    return_data.append(dict(id=2, name=lazy_gettext('Me and Band Members'), email=email))

    email = email.replace(current_user.email + ',', '')

    return_data.append(dict(id=3, name=lazy_gettext('Band Members'), email=email))

    return jsonify(data=return_data)


@app.route('/pdf-options/')
@login_required
def pdf_options():
    """
    Returns the available pdf options for sharing setlists
    :return: The pdf options
    """
    # noinspection PyListCreation
    return_data = []
    return_data.append(dict(id=1, name=lazy_gettext('Sequence number')))
    return_data.append(dict(id=2, name=lazy_gettext('Artist')))
    return_data.append(dict(id=3, name=lazy_gettext('Key')))
    return_data.append(dict(id=4, name=lazy_gettext('Tempo')))

    return jsonify(data=return_data)


@app.route('/delete-show', methods=["POST"])
@login_required
def delete_show():
    """
    Deletes a show and it's setlist
    :return: Info message
    """
    show = Show.query.get(int(request.form.get('id')))
    db.session.delete(show)
    return jsonify(dict(msg=gettext('Show successfully deleted.')))


@app.route('/fetch-available-songs/<show_id>/<filtered_band_id>', methods=['GET'])
@login_required
def fetch_available_songs(show_id, filtered_band_id):
    """
    Fetch all the available songs of the current user from his or her Song Catalogue
    not yet added to a given show's setlist
    :param filtered_band_id: to filter from which associated band the song comes from
    :param show_id: to prevent duplicate songs
    :return: JSON with the songs list
    """

    available_songs = current_user.songs.order_by(Song.title).all()

    show = Show.query.get(show_id)
    show_songs = show.songs

    # Remove already added songs to the setlists. Return only leftovers songs
    for show_song in show_songs:
        for available_song in available_songs:
            if show_song.id == available_song.id:
                available_songs.remove(available_song)

    return_data = []
    for song in available_songs:
        # Now we check if the song belongs to the filteredband (-1 = all)
        if int(filtered_band_id) == -1:
             return_data.append(dict(id=song.id, title=song.title + ' (' + song.artist + ')'))
        else:
            for band in song.bands:
                if band.id == int(filtered_band_id):
                    return_data.append(dict(id=song.id, title=song.title + ' (' + song.artist + ')'))



    return jsonify(data=return_data)


@app.route('/fetch-setlist/<int:show_id>', methods=['GET'])
@login_required
def fetch_setlist(show_id):
    """
    Fetch a show's setlist (added songs)
    :return: JSON with the songs list
    """
    show = Show.query.get(show_id)
    setlist = show.songs

    return_data = []
    for song in setlist:
        return_data.append(
            dict(id=song.id, title=song.title, tempo=song.tempo, artist=song.artist, duration=song.pretty_duration(),
                 lyrics=song.lyrics))

    return jsonify(data=return_data)


@app.route('/add-song', methods=["POST"])
@login_required
def add_song():
    """
    Adds a song to a show setlist
    :return: the song just added
    """
    show = Show.query.get(int(request.form.get('showid')))
    song = Song.query.get(int(request.form.get('songid')))
    show.add_song(song)
    db.session.add(show)
    db.session.commit()
    show.assign_position(song)
    return jsonify(dict(id=song.id, title=song.title, artist=song.artist, duration=song.pretty_duration()))


@app.route('/save-setlist', methods=["POST"])
@login_required
def save_setlist():
    """
    Saves the sorted setlist
    :return: empty dict
    """
    show = Show.query.get(int(request.form.get('showid')))

    # First we delete the previous songs, so we don't have to deal with updates
    show.remove_all_songs()

    # Now we add the new, sorted, setlist
    song_ids = request.form.get('songIds').split(',')

    pos = 1

    for song_id in song_ids:
        song = Song.query.get(song_id)
        show.add_song(song)
        db.session.add(show)
        db.session.commit()
        show.assign_position(song, pos)
        pos += 1

    return jsonify(dict())


@app.route('/remove-from-setlist', methods=["POST"])
@login_required
def remove_from_setlist():
    """
    Removes a song from a show's setlist
    :return: empty dict
    """
    show = Show.query.get(int(request.form.get('showid')))
    song = Song.query.get(int(request.form.get('songid')))
    show.remove_song(song)
    db.session.commit()
    return jsonify(dict(id=song.id, title=song.title + ' (' + song.artist + ')', duration=song.pretty_duration()))


@app.route('/move-down', methods=["POST"])
@login_required
def move_down():
    """
    Moves a song down (increment order) in the show's setlist
    :return: empty dict
    """
    show = Show.query.get(int(request.form.get('showid')))
    song = Song.query.get(int(request.form.get('songid')))
    show.move_down(song)
    return jsonify(dict())


@app.route('/move-up', methods=["POST"])
@login_required
def move_up():
    """
    Moves a song up (decrement order) in the show's setlist
    :return: empty dict
    """
    show = Show.query.get(int(request.form.get('showid')))
    song = Song.query.get(int(request.form.get('songid')))
    show.move_up(song)
    return jsonify(dict())


@app.route('/perform/', methods=["GET"])
@login_required
def perform():
    """
    Shows the setlist in Perform Mode
    :return: the rendered Perform page
    """
    if request.method == 'GET':
        showid = request.args.get('id')

        # Edit Song
        if showid is not None:
            show = Show.query.get(int(showid))

            if not is_current_user(show.user_id):
                return render_template("not-authorized.html")

            start_date = format_datetime(show.start, get_date_format(fullformat=False))

            return render_template("perform.html", show_description=show.name + ' (' + start_date + ')',
                                   show_id=show.id, show_length=len(show.songs.all()))


@app.route('/share-setlist', methods=["POST"])
@login_required
def share_setlist():
    """
    Sends by email a setlist to the chosen recipients in the chosen format (txt or pdf)
    :return: Success message
    """
    show = Show.query.get(int(request.form.get('showid')))
    share_songs = show.songs

    if request.form.get('recipients') == '':
        share_recipients = [current_user.email]  # Default recipient
    else:
        share_recipients = request.form.get('recipients').split(',')

    file_format = int(request.form.get('format'))

    start_date = format_datetime(show.start, get_date_format(fullformat=False))
    nr_songs = str(len(share_songs.all())) + ' ' + gettext('songs')

    subject = gettext('Setlist for ') + show.name + ' (' + start_date + ')'
    body = gettext('This Setlist was sent from Songlist Plus\n\n')
    pdf = None

    if file_format == 1:  # TXT
        setlist_txt = ''
        for song in share_songs:
            setlist_txt += song.title + '\n'
        body += setlist_txt

    else:  # PDF
        if request.form.get('options') != '':
            options = request.form.get('options').split(',')
            sequence_nr = True if '1' in options else False
            artist = True if '2' in options else False
            key = True if '3' in options else False
            tempo = True if '4' in options else False

        template = render_template('setlist.html', title=show.name, songs=share_songs, sequence_nr=sequence_nr,
                                   artist=artist, key=key, tempo=tempo, start_date=start_date, nr_songs=nr_songs)
        pdf = create_pdf(template)

    try:
        send_email(share_recipients, subject, body, pdf)
    except:
        return jsonify(dict(msg=gettext(
            'An error occurred while sending your Setlist. Please contact the administrator. We are sorry for the incovenience.')))
    else:
        return jsonify(dict(msg=gettext('The Setlist was sent to the chosen recipients')))


@app.route('/export-songs', methods=["GET"])
@login_required
def export_songs():
    """
    Exports the user songs to JSON format
    :return: JSON file
    """

    song_database = current_user.songs.order_by(Song.title).all()  # All the current user songs
    song_ids = []

    # List of song ids
    for song in song_database:
        song_ids.append(song.id)

    d = dict()
    d['user_id'] = current_user.id
    d['song_ids'] = song_ids

    export_json = jsonify(d)  # Songs in json format

    response = make_response(export_json)
    response.headers["Content-Disposition"] = "attachment; filename=songs.json"

    return response


@app.route('/import-songs', methods=["POST"])
@login_required
def import_songs():
    """
    Imports songs from a JSON file to the current user
    :return: Success message
    """

    if 'file' not in request.files:
        flash(gettext('File not found'))
        return render_template("songs.html")

    file = request.files['file']

    if file.filename == '':
        flash(gettext('File not found'))
        return render_template("songs.html")

    if not allowed_file(file.filename, ['json']):
        flash(gettext('File not allowed'))
        return render_template("songs.html")

    if file:
        file.seek(0)
        contents = loads(file.read().decode('utf-8'))

        count = 0

        for song_id in contents['song_ids']:
            original_song = Song.query.get(int(song_id))

            if original_song:
                copy_song = Song(title=original_song.title, artist=original_song.artist, key=original_song.key,
                                 tempo=original_song.tempo,
                                 duration=original_song.duration, notes=original_song.notes,
                                 lyrics=original_song.lyrics,
                                 user_id=current_user.id)
                db.session.add(copy_song)
                count += 1

        flash(gettext(str(count) + ' songs successfully added'))
        return render_template("songs.html")
