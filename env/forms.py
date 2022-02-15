from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TimeField, SelectField
import random

wordlist = ["Hello","World","Print","My","Name","Is","Random"]

class Login(FlaskForm):
    id = IntegerField('ID')
    uname = StringField('uname')
    passwd = PasswordField('passwd')
    submit = SubmitField('Sign Up')

class InteractiveForm2(FlaskForm):
    bus = StringField('BUS')
    city = StringField('CITY')
    time = TimeField('TIME')
    search = SubmitField('SEARCH')

class InteractiveForm(FlaskForm):
    p1 = StringField('Input')
    p2 = StringField('Input')
    submit = SubmitField('Submit')



class RandomForm(FlaskForm):
    i = 0 # TODO change this to an environment variable in env.yaml
    fields = {}
    submit = SubmitField('Submit')

    while i < 2: # TODO change this to an environment variable in env.yaml
        # dynamically create param name
        data = StringField(str(random.choice(wordlist)))

        # calculate value

        i += 1
    print(fields)







