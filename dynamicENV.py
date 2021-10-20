import os
import sys
import random
import yaml
from flask import Flask, render_template, url_for, redirect, request, g
from env.forms import Login, InteractiveForm, RandomForm
import sqlite3
from env.html_generator import *
from faker import Faker
from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from env.sqlQueries import booleanBased, unionBased


app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 5000

fake = Faker()


# File structuring
dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'config\env.yaml')
wordlist_path = os.path.join(dirname, 'env\wordlists\engWord')
templates_path = os.path.join(dirname, 'templates')
templates = os.listdir(templates_path)

# Static database locations
account_db_path = os.path.join(dirname, 'env\\accounts.db')
bus_db_path = os.path.join(dirname, 'env\\busservice.db')
test_db_path = os.path.join(dirname, 'env\\test.db')

# Security key required for Flask-WTF. This can be anything
app.config['SECRET_KEY'] = 'demo_ctf'


def read_config():
    stream = open(config_path, 'r')
    data = yaml.load(stream)

    vulnerability_config = data[0]
    database_config = data[1]
    HTML_config = data[2]
    security_config = data[3]


    return database_config, HTML_config, vulnerability_config, security_config

def challenge_type():
    config = read_config()

    vulnerability_config = config[2]

    if "boolean" in vulnerability_config["details"]["vulnerability_type"]:
        query = booleanBased()
    elif "union" in vulnerability_config["details"]["vulnerability_type"]:
        query = unionBased()
    return query

challenge = challenge_type()



def wordlists():
    wordlistFile = open(wordlist_path, 'r')
    wordlist = []
    for word in wordlistFile:
        word = word.strip()
        wordlist.append(word)

    return wordlist

def isRandom():
    config = read_config()

    database_config = config[0]
    HTML_config = config[1]

    if database_config["database"]["randomised_content"] == 1:
        database_config_random = True

        wordlists()
    else:
        database_config_random = False

    if HTML_config["interaction"]["randomised_content"] == 1:
        HTML_config_random = True

        wordlists()
    else:
        HTML_config_random = False

    return database_config_random, HTML_config_random

def genDB():



    # generate dummy data object
    fake_data = defaultdict(list)

    # Create dummy data
    for _ in range (1000):
        fake_data["first_name"].append(fake.first_name())
        fake_data["last_name"].append(fake.last_name())
        fake_data["occupation"].append(fake.job())
        fake_data["dob"].append(fake.date_of_birth())
        fake_data["country"].append(fake.country())

    # Export data to pandas dataframe
    df_fake_date = pd.DataFrame(fake_data)

    global filename
    filename = "testdb.db" # TODO change to dynamic variable rather than static assignment
    format = "sqlite:///"
    url = os.path.join(format, filename)

    ### Create the database
    engine = create_engine(url) # URL formatting can be changed to MySQL, POSTGRS if needed
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        pass


    # Export dataframe to database
    try:
        df_fake_date.to_sql('user', con=engine, index=False) # First 'entry' will be a table name e.g. 'user' = table name
    except:
        pass


    try:
        df_fake_date.to_sql('account', con=engine, index=False)
    except:
        pass

def test_connection():

    con = sqlite3.connect("testdb.db")
    cursor = con.cursor()

    select = "SELECT first_name FROM user UNION ALL SELECT last_name FROM account"

    data = []
    for raw in cursor.execute(select):
        data.append(raw)


    return data

def interaction():
    pass




def setup_site():

    read_config()
    isRandom()
    wordlists()

    ### Check for random content set
    random_check = isRandom()

    ### Check 1 is HTML_config_random
    if random_check[1] is True:

        # get random words for testing
        randomwords = wordlists()
        random_name_test = random.choice(randomwords)

        random_params = random.sample(randomwords, 2)

        print("What")

        @app.route("/", methods=["GET", "POST"])
        def index():
            #data = test_connection()
            #print(data)

            form = InteractiveForm()
            query = challenge

            interaction1 = request.form.get('p1')
            interaction2 = request.form.get('p2')

            sql = query + "'{}'".format(interaction2)

            con = sqlite3.connect("testdb.db")
            cursor = con.cursor()


            cursor.execute(sql)

            #cursor.execute("SELECT * FROM user WHERE last_name ='{}'".format(interaction2))

            db_data = cursor.fetchall()


            return render_template("random_index.html", form=form, returned = db_data, random_message=query) # random_content=data

        def restart():
            @app.route("/restart", methods=["GET", "POST"])
            def test():
                os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
                return "Restarting application"

        restart()

        @app.route("/index", methods=["GET", "POST"])
        def random_index():

            random_greeting = random_name_test
            form = RandomForm()

            return render_template("random_index.html", random_content = random_greeting, random_form = form)

    else:
            @app.route("/test2", methods=["GET, POST"])
            def static_index():
                print("Test")
                return render_template("index.html")


setup_site()
genDB()
test_connection()


if __name__ == "__main__":
    app.run(host=HOST, port=PORT,debug = False)

    #app.run(host=HOST, port=PORT) ### TODO Disable 'debug = true' in production as it runs Flask twice causing db issues
    #debug=True

