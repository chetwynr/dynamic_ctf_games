import random


def get_schema():
    schema = "PRAGMA table_info('user')"
    #schema = """
                 #select group_concat(name,'|') from pragma_table_info("table_name")
                #"""
    return schema


def string_delimiter():
    delimiter = [
        "'", '"'
    ]
    random_delimiter = random.choice(delimiter)
    return random_delimiter

def commend_delimiter():
    delimiter = [
        "--", "#", "/*"
    ]
    random_delimiter = random.choice(delimiter)
    return random_delimiter

### Static Queries

### TODO Generate a series of static queries
def booleanBased():
    queries = [
        "SELECT * FROM user WHERE col0 =",
        "SELECT col1 FROM user WHERE col2 =",
        "SELECT col0, col3, col2 FROM user WHERE col4 =",
        "SELECT * FROM user WHERE col2 =",
        "SELECT * FROM user WHERE col4 ="
    ]
    random_query = random.choice(queries)
    return random_query


'''def booleanBased():
    queries = [
        "SELECT * FROM user WHERE col1 =",
        "SELECT first_name FROM user WHERE last_name =",
        "SELECT first_name, last_name, dob FROM user WHERE occupation =",
        "SELECT * FROM user WHERE occupation =",
        "SELECT * FROM user WHERE first_name ="
    ]
    random_query = random.choice(queries)
    return random_query
'''
def unionBased():
    queries = [
        "SELECT col0 FROM user UNION ALL SELECT col1 from account where col3 =",
        "SELECT col2 FROM user UNION ALL SELECT col1 from account where col0 =",
        "SELECT col3 FROM user UNION ALL SELECT col2 from account where col2 =",
        "SELECT col4 FROM user UNION ALL SELECT col3 from account where col0 ="
    ]
    random_query = random.choice(queries)
    return random_query


def timeBased():
    queries = [

    ]
    random_query = random.choice(queries)
    return random_query

def ErrorBased():
    queries = [

    ]
    random_query = random.choice(queries)
    return random_query
