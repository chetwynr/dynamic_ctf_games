import sqlite3
from sqlite3 import Error
import yaml
from yaml.loader import SafeLoader
import random

#print(os.getcwd())

config_path = "C:\\Users\\roberac\\PycharmProjects\\dynamic_ctf_games\\config\\env.yaml"
wordlist_path = "C:\\Users\\roberac\\PycharmProjects\\dynamic_ctf_games\\env\\wordlists\\engWord"
wordlistFile = open(wordlist_path, 'r')
wordlist = []
for word in wordlistFile:
    word = word.strip()
    wordlist.append(word)

# Create wordlist set for randomised naming


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

        conn = None

        # Bool logic for randomised database generation
        if int(database_config["database"]["randomised_content"]) == 1:
            try:
                randomdbName = random.choice(wordlist)
                randomdbName = str(randomdbName+".db")


                #conn = sqlite3.connect(str(dbName)[1:-1][1:-1] + ".db")
                conn = sqlite3.connect(randomdbName)
                print(sqlite3.version)

                return randomdbName

            except Error as e:
                print(e)
            finally:
                if conn:
                    conn.close()

        else:
            random_content = False

    #randomdbName = create_db()

    def create_table():

        conn = None
        i = 0

        if int(database_config["database"]["randomised_content"]) == 1:
            try:


                while i < tables_count:
                    print(i)
                    conn = sqlite3.connect(randomdbName)
                    randomtbName = random.sample(wordlist, tables_count)
                    tbName = str(randomtbName[i])
                    cursor = conn.cursor()
                    cursor.execute("CREATE TABLE " +tbName + "(hello INTEGER PRIMARY KEY, world TEXT UNIQUE)")

                    print(tbName)
                    i+=1

            except Error as e:
                print(e)
        else:
            random_content = False

    create_db()
    create_table()

def random_name():
    return randomdbName




database_config()
