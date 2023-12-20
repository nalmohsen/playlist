"""Forms for playlist app."""

from wtforms import SelectField, StringField, TextAreaField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""
    
    name = StringField("Playlist Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Create Playlist")

class SongForm(FlaskForm):
    """Form for adding songs."""
    
    title = StringField('Song Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    submit = SubmitField('Add Song')

# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""
    
    song = SelectField('Song To Add', coerce=int)
