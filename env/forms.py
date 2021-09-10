from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField

class Login(FlaskForm):
    id = IntegerField('ID')
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sign Up')