import sqlite3
import os

'''

Currently static interactions and analysis with the sister.db test database

This database was randomly generated using the database.py module

'''
def create_TestDB():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE test1(username TEXT PRIMARY KEY, password TEXT)")
    cursor.execute("CREATE TABLE test2(username TEXT PRIMARY KEY, password TEXT)")
    cursor.execute("INSERT INTO test1 (username, password) VALUES('hello','world')")
    cursor.execute("INSERT INTO test2 (username, password) VALUES('admin','12345')")

    conn.commit()


def lookup_data():

    # Define the database we interact with and create a cursor connection for SQL interaction
    con = sqlite3.connect('cloud.db')
    cursor = con.cursor()

    # Input our SQL lookup commands here
    #cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    cursor.execute("SELECT * FROM jacket")


    # Use this function to printout all the data discovered
    #print(cursor.fetchall())

    for item in cursor:
        print(item)


    con.close()

def input_data():

    # Define the database we interact with and create a cursor connection for SQL interaction
    con = sqlite3.connect('cloud.db')
    cursor = con.cursor()

    # Input our test data here
    #cursor.execute("INSERT INTO heavy values (1,'john','password1')")
    #cursor.execute("INSERT INTO heavy values(2,'ringo','Starr')")
    #cursor.execute("INSERT INTO heavy values(3,'flag','{SQL-CTF-32irj2dijr982u90ikjlkjliu0981jad}')")

    #cursor.execute("CREATE TABLE heavy(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

    # This commits the changes and updates the database. Without this no changes will be saved
    con.commit()

    con.close()

def show_tables():
    con = sqlite3.connect('cloud.db')
    cursor = con.cursor()


    # Input our test data here
    cursor.execute("select name from sqlite_master where type='table' and name NOT LIKE 'sqlite_%'")
    print(cursor.fetchall())

    con.close()

def show_columns():
    con = sqlite3.connect('busservice.db')
    cursor = con.cursor()


    # Input our test data here
    #cursor.execute("PRAGMA table_info(service)")
    cursor.execute("PRAGMA table_info(serviceAdmin)")
    print(cursor.fetchall())

    con.close()

def insert_flag():
    flag = "CTF-SQL{W3lc0m3-H0m3-C0mM4nD3r}"
    con = sqlite3.connect("busservice.db")
    cursor = con.cursor()

    cursor.execute("INSERT INTO serviceAdmin (service, city, time) VALUES('11','"+flag+"','22:22')")

    con.commit()
#input_data()
#lookup_data()
#show_columns()
#show_tables()
#insert_flag()
create_TestDB()