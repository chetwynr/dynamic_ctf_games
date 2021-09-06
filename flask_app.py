# A deliberately vulnerable - non secure Dynamic CTF environment

import sys
import yaml

config_path = "C:\\Users\\roberac\\PycharmProjects\\dynamic_ctf_games\\config\\env.yaml"
from flask import Flask, render_template
#from env.database import random_name

app = Flask(__name__)

def site_config():
    stream = open(config_path, 'r')
    data = yaml.load(stream)

    app_config = data[2] ### data[2] is 'interaction' subsection in the env.yaml file

### Define bool logic here for configuring the site - based upon the content of the YAML file
### Define directories and subdirectories via app.route

    if "login" in app_config["interaction"]["form_type"]:
        if app_config["interaction"]["randomised_content"] == 0:
            try:
                @app.route("/")
                def home():
                    return render_template("static_simple_login.html")
            except:
                return "Generic Error - Needs refining"
        else:
            return "Random specified"



if __name__ == "__main__":
    app.run(debug=True)

site_config()