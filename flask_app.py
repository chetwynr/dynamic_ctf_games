# A deliberately vulnerable - non secure Dynamic CTF environment

import sys
import yaml

config_path = "C:\\Users\\roberac\\PycharmProjects\\dynamic_ctf_games\\config\\env.yaml"

from flask import Flask, render_template
from env.forms import Login

app = Flask(__name__)

# Security key required for Flask-WTF. This can be anything
app.config['SECRET_KEY'] = 'demo'

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
                    return render_template("static_simple_login.html")

                @app.route("/login", methods=["GET","POST"])
                def login():
                    form = Login()
                    return render_template("static_login.html", form=form)
            except:
                return "Generic Error - Needs refining"
        else:
            return "Random specified"



if __name__ == "__main__":
    app.run(debug=True)

site_config()