# A deliberately vulnerable - non secure Dynamic CTF environment

import os
import sys
import yaml
from flask import Flask, render_template, url_for, redirect, request, g
from env.forms import Login
import sqlite3

app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 3200

dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'config\env.yaml')
db_path = os.path.join(dirname, 'env\sister.db')


# Security key required for Flask-WTF. This can be anything
app.config['SECRET_KEY'] = 'demo_ctf'

def site_config():
    stream = open(config_path, 'r')
    data = yaml.load(stream)

    app_config = data[2] ### data[2] is 'interaction' subsection in the env.yaml file

### Define bool logic here for configuring the site - based upon the content of the YAML file
### Define directories and subdirectories via app.route

    if "login" in app_config["interaction"]["form_type"]:
        if app_config["interaction"]["randomised_content"] == 0:
            try:
                @app.route("/", methods=["GET", "POST"])
                def home():

                    return render_template("index.html")

                @app.route("/login", methods=["GET","POST"])
                def login():

                    form = Login()

                    return render_template("static_login.html", form=form)


                ### Route for testing database query responses. Currently this returns the entire contents of the DB to the user
                @app.route("/list", methods=["GET","POST"])
                def list():
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    cursor.execute("select * from heavy")
                    db_data = cursor.fetchall()

                    return render_template("list.html", database=db_data)




            except:
                return "Generic Error - Needs refining"
        else:
            return "Random specified"



site_config()

if __name__ == "__main__":
    app.run(host=HOST,port=PORT,debug=True)