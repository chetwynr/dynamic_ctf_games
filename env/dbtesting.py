import sqlite3

'''

Currently static interactions and analysis with the sister.db test database

This database was randomly generated using the database.py module

'''


def lookup_data():

    # Define the database we interact with and create a cursor connection for SQL interaction
    con = sqlite3.connect('sister.db')
    cursor = con.cursor()

    # Input our SQL lookup commands here
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    cursor.execute("SELECT * FROM heavy")


    # Use this function to printout all the data discovered
    print(cursor.fetchall())


    con.close()


def input_data():

    # Define the database we interact with and create a cursor connection for SQL interaction
    con = sqlite3.connect('sister.db')
    cursor = con.cursor()


    # Input our test data here
    cursor.execute("INSERT INTO heavy values (1,'john','password1')")
    cursor.execute("INSERT INTO heavy values(2,'ringo','Starr')")
    cursor.execute("INSERT INTO heavy values(3,'flag','{SQL-CTF-32irj2dijr982u90ikjlkjliu0981jad}')")


    # This commits the changes and updates the database. Without this no changes will be saved
    con.commit()

    con.close()

input_data()
lookup_data()