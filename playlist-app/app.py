from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/playlist-app'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize Flask-Migrate
migrate = Migrate(app, db)

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")

# Playlist routes
@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    
    playlist = Playlist.query.get_or_404(playlist_id)
    songs = Song.query.join(PlaylistSong).filter(PlaylistSong.playlist_id == playlist_id).all()
    
    return render_template("playlist.html", playlist=playlist, songs=songs)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form."""
    
    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        playlist = Playlist(name=name, description=description)
        db.session.add(playlist)
        db.session.commit()
        return redirect("/playlists")

    return render_template("new_playlist.html", form=form)

# Song routes
@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a specific song."""
    
    song = Song.query.get_or_404(song_id)
    
    return render_template("song.html", song=song)

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form."""
    
    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data

        # Create a new song and add it to the database
        song = Song(title=title, artist=artist)
        db.session.add(song)
        db.session.commit()

        return redirect("/songs")

    return render_template("new_song.html", form=form)

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist."""
    
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    curr_on_playlist = [song.id for song in playlist.songs]
    form.song.choices = [(song.id, song.title) for song in Song.query.all() if song.id not in curr_on_playlist]

    if form.validate_on_submit():
        song_id = form.song.data
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)
