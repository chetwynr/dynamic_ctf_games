from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TimeField, SelectField
import random

wordlist = ["Hello","World","Print","My","Name","Is","Random"]

class Login(FlaskForm):
    id = IntegerField('ID')
    uname = StringField('uname')
    passwd = PasswordField('passwd')
    submit = SubmitField('Sign Up')

class InteractiveForm(FlaskForm):
    bus = StringField('BUS')
    city = StringField('CITY')
    time = TimeField('TIME')
    search = SubmitField('SEARCH')

class newEpisode(FlaskForm):
    newEpisode = StringField("New Episode?")
    episodeSubmit = SubmitField("Choose")




