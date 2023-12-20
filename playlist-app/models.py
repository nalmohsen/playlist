"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist."""
    
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    
    # Define the relationship with Song
    songs = db.relationship('Song', secondary='playlist_songs', backref='playlists')

class Song(db.Model):
    """Song."""
    
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    artist = db.Column(db.String(100), nullable=False)  

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    
class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""
    
    __tablename__ = 'playlist_songs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)
