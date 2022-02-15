import os
import sys
import random
import urllib.parse
import yaml
from flask import Flask, render_template, url_for, redirect, request, g
from env.forms import Login, InteractiveForm, RandomForm
import sqlite3
from env.html_generator import *
from faker import Faker
from faker.providers import barcode, internet, file
from collections import defaultdict
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData
import pandas as pd
from env.sqlQueries import booleanBased, unionBased, get_schema
#from env.sqlQueries import get_schema
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 5000

#meta = MetaData()
fake = Faker()

### create DB at start. Dummy credentials used
#mydb = mysql.connector.connect(host="localhost",user="",password="")
#mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE test")

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


def read_config(): # logic for reading env.yaml file configurations
    stream = open(config_path, 'r')
    data = yaml.load(stream)

    vulnerability_config = data[0]
    database_config = data[1]
    HTML_config = data[2]
    security_config = data[3]


    return database_config, HTML_config, vulnerability_config, security_config

def challenge_type(): # logic for choosing SQL Queries based on defined SQLi challenge type
    config = read_config()

    vulnerability_config = config[2]

    if "boolean" in vulnerability_config["details"]["vulnerability_type"]:
        query = booleanBased()
        #query = get_schema()
    elif "union" in vulnerability_config["details"]["vulnerability_type"]:
        query = unionBased()
        #query = get_schema()
    return query


challenge = challenge_type() # Assigned outside of function otherwise a new query is generated each time a POST request is made



def wordlists():    # random word(s) generation
    wordlistFile = open(wordlist_path, 'r')
    wordlist = []
    for word in wordlistFile:
        word = word.strip()
        wordlist.append(word)

    return wordlist

def isRandom(): # logic for checking if random content is supplied. If not the system will use predefined static templates
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

def genDB(db_username, db_password, db_host, db_port): ### Database generation logic - includes dummy data generation, DB configuration & generation



    # generate dummy data object
    fake_data = defaultdict(list)


    # Testing for random column names
    # TODO variable types, column name export



    global filename
    filename = "testing.db" # TODO change to dynamic variable rather than static assignment

    config = read_config()
    format_check = config[0]

    # generate dummy data object
    fake_data = defaultdict(list)
    random_string = wordlists()


    max = 5
    global count
    count = 0

    list_col_names_for_saving = []

    # Create dummy data python with completely random data type and column names
    # Needs fixing
    #def gen_totally_randomDB():
    #    while count < max:
    #        randomised_choice = random.choice(random_string)
    #        list_col_names_for_saving.append(randomised_choice)
    #        randomised_provider = random.choice(fake.last_name())
    #        string_conversion = str(randomised_choice)
    #        for _ in range (1000):
    #            print(string_conversion)
    #            #fake_data[str(string_conversion)].append(fake.first_name())
    #            fake_data[str(string_conversion)].append(randomised_provider)
    #        count +=1



    # Create dummy data
    while count < 5:
        fake_date = {}
        i = count
        data_type = [fake.first_name(), fake.last_name(), fake.date_of_birth(), fake.job(), fake.country()]
        random_type = random.choice(data_type)
        col_value = str(count)
        fake_data["col"+col_value]
        for _ in range (1000):
            fake_data["col"+col_value].append(random_type)
        count +=1
            #fake_data["last_name"].append(fake.last_name())
            #fake_data["occupation"].append(fake.job())
            #fake_data["dob"].append(fake.date_of_birth())
            #fake_data["country"].append(fake.country())

    # Export data to pandas dataframe
    df_fake_date = pd.DataFrame(fake_data)

    password = urllib.parse.quote_plus(db_password) # Password is encoded for database connection

    ### Logic for database system of choice
    if "sqlite" in format_check["database"]["type"]:
        format = "sqlite:///"

    ### Following formats will error if not present on host system
    elif "mysql" in format_check["database"]["type"]:
        format = "mysql://{}:{}@{}:{}/{}".format(db_username, password, db_host, db_port, filename)
    elif "microsoft_sql" in format_check["database"]["type"]:
        format = "mysql:///"
    elif "postgresql" in format_check["database"]["type"]:
        format = "postgresql:///"
    elif "oracle" in format_check["database"]["type"]:
        format = "oracle:///"

    url = os.path.join(format,filename)
    #url = os.path.join(format)
    #print(url)

    ### Create the database
    engine = create_engine(url)
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
        df_fake_date.to_sql('account', con=engine, index=False) # First 'entry' will be a table name e.g. 'account' = table name
    except:
        pass


def test_connection(): ### Currently not in use, exists for DB testing


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


        @app.route("/", methods=["GET", "POST"])
        def index():

            form = InteractiveForm()
            query = challenge

            interaction1 = request.form.get('p1')
            interaction2 = request.form.get('p2')

            interaction_param = [interaction1, interaction2]

            sql = query + "'{}'".format(interaction2)

            print(sql)

            ### TODO make seperate conns for each db type

            ### Con for sqlite3
            con = sqlite3.connect("testing.db")
            cursor = con.cursor()

            cursor.execute(sql)
            # cursor.execute(query)

            ### con for mysql
            #con = mysql.connector.connect(user='root', password='', host='127.0.0.1', port=3306, database='testing')
            #cursor = con.cursor()

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



if __name__ == "__main__":

    setup_site()

    ### If no args are supplied then use the following defaults. Applies to all formats but SQLite
    if len(sys.argv) < 4:
        db_username = "root"
        db_password = "" ### Enter Credentials
        db_host = "127.0.0.1"
        db_port = 3306

        genDB(db_username, db_password, db_host, db_port)
    else:
        genDB(
            str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4])
        )
    #test_connection()

    app.run(host=HOST, port=PORT,debug = False)

    #app.run(host=HOST, port=PORT) ### TODO Disable 'debug = true' in production as it runs Flask twice causing db issues
    #debug=True

