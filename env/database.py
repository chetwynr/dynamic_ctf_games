import os
import sqlite3
from sqlite3 import Error
import yaml
import csv
from yaml.loader import SafeLoader
import random

### Get configuration file
dirname = os.path.dirname(os.path.dirname(__file__))
config_path = os.path.join(dirname, 'config\env.yaml')


### Get wordlist
dirname = os.path.dirname(__file__)
wordlist_path = os.path.join(dirname, 'wordlists\engword')
account_path = os.path.join(dirname, 'wordlists\city_service.csv')
service_path = os.path.join(dirname, 'wordlists\service.txt')


wordlistFile = open(wordlist_path, 'r')
wordlist = []
for word in wordlistFile:
    word = word.strip()
    wordlist.append(word)


### Read YAML Database Configuration
def database_config():
    stream = open(config_path, 'r')
    data = yaml.load(stream)

    database_config = data[1]

    i = 0

    #print("Database Content:")
    #print(database_config["database"])


    tables_count = int(database_config["database"]["max_tables"])
    columns_count = int(database_config["database"]["max_columns"])

    def create_db():
        global randomdbName
        global staticdbName

        staticdbName = "busservice.db"

        conn = None

        # Bool logic for randomised database generation
        if int(database_config["database"]["randomised_content"]) == 1:
            try:
                randomdbName = random.choice(wordlist)
                randomdbName = str(randomdbName+".db")


                conn = sqlite3.connect(randomdbName)

                return randomdbName

            except Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()

        ### Configurations for static database
        else:
            try:
                conn = sqlite3.connect(staticdbName)

            except Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()



    def create_table():

        conn = None
        i = 0

        if int(database_config["database"]["randomised_content"]) == 1:
            try:

                randomtbName = random.sample(wordlist, tables_count)

                while i < tables_count:

                    conn = sqlite3.connect(randomdbName)
                    tbName = str(randomtbName[i])
                    cursor = conn.cursor()

                    cursor.execute("CREATE TABLE {}(id TEXT PRIMARY KEY, username TEXT, password TEXT)".format(tbName))
                    conn.commit()

                    ### Insert demo account data for username/password login
                    with open(account_path) as f:
                        account_data = f.readlines()

                        for account in account_data:
                            input = account.split(",")

                            conn = sqlite3.connect(randomdbName)
                            cursor = conn.cursor()

                            cursor.execute("INSERT INTO {} (id, username, password) VALUES ('{}','{}','{}')".format(tbName,input[0],input[1],input[2]))
                            conn.commit()

                    i+=1
                    conn.commit()

                return randomtbName

            except Error as e:
                print(e)
        else:
            static_tableName = ["service","serviceAdmin"]
            for entry in static_tableName:

                tableName = str(entry)
                conn = sqlite3.connect(staticdbName)
                cursor = conn.cursor()

                cursor.execute("CREATE TABLE {}(service TEXT PRIMARY KEY, city TEXT, time TEXT)".format(tableName))

                with open(account_path) as f:
                    account_data = f.readlines()

                    for account in account_data:
                        input = account.split(",")

                        conn = sqlite3.connect(staticdbName)
                        cursor = conn.cursor()

                        cursor.execute(
                            "INSERT INTO {} (service, city, time) VALUES ('{}','{}','{}')".format(tableName, input[0],
                                                                                                     input[1],
                                                                                                     input[2]))
                        conn.commit()
                conn.commit()









    create_db()
    create_table()

def random_name():
    return randomdbName




database_config()
