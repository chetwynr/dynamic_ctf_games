# A deliberately vulnerable - non secure Dynamic CTF environment

# TODO: Refreshing function for HTML - SQL content

import os
import random
import sys
import yaml
from flask import Flask, render_template, url_for, redirect, request, g
from env.forms import Login, InteractiveForm, newEpisode
import sqlite3

app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 5000

dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'config\env.yaml')
templates_path = os.path.join(dirname, 'templates')

### Static database configuration
account_db_path = os.path.join(dirname, 'env\\accounts.db')
bus_db_path = os.path.join(dirname, 'env\\busservice.db')
test_db_path = os.path.join(dirname, 'env\\test.db')

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

                @app.route("/testing", methods=["GET", "POST"])
                def testing():

                    form = newEpisode()

                    templates = os.listdir(templates_path)


                    check = request.form.get("newEpisode")

                    try:
                        if "Y" in check:
                            new_template = random.choice(templates)
                            return render_template(new_template, form=form)
                        else:
                            return render_template("testing.html", form=form)
                    except:
                        return render_template("testing.html", form=form)


                ### Example route for listing database contents
                @app.route("/list", methods=["GET","POST"])
                def list():

                    conn = sqlite3.connect(account_db_path)
                    cursor = conn.cursor()
                    form = Login()
                    db_username = request.form.get('uname')
                    db_password = request.form.get('passwd')


                    cursor.execute("SELECT * FROM userAccounts WHERE username ='{}'".format(db_username))
                    #cursor.execute("SELECT * FROM heavy WHERE username =(?)", (db_username,))

                    db_data = cursor.fetchall()

                    return render_template("static_login.html", form=form, database=db_data, greeting=db_username)

                @app.route("/login", methods=["GET", "POST"])
                def login():

                    form = Login()

                    return render_template("static_login.html", form=form)
            except:
                    return "Generic Error - Needs refining"


    elif "interactive" in app_config["interaction"]["form_type"]:
        @app.route("/", methods=["GET", "POST"])
        def home():

            return render_template("index.html")

        @app.route("/service", methods=["GET", "POST"])
        def service():

            conn = sqlite3.connect(bus_db_path)
            #conn = sqlite3.connect(test_db_path)
            cursor = conn.cursor()
            form = InteractiveForm()

            bus = request.form.get('bus')
            city = request.form.get('city')

            cursor.execute("SELECT * FROM service WHERE service = '%s'" %bus)


            #cursor.execute("SELECT city, time FROM service UNION SELECT city, time FROM serviceAdmin where service ='2'")






            db_data = cursor.fetchall()

            return render_template("bus_service.html", form=form, database=db_data)



site_config()

if __name__ == "__main__":

    stream = open(config_path, 'r')
    data = yaml.load(stream)
    security_config = data[3]

    if security_config["security"]["security_level"] == 0:
        app.run(host=HOST,port=PORT,debug=True)
    else:
        app.run(host=HOST, port=PORT, debug=False)