import random

def booleanBased():
    queries = [
        "SELECT * FROM user WHERE last_name =",
        "SELECT first_name FROM user WHERE last_name =",
        "SELECT first_name, last_name, dob FROM user WHERE occupation =",
        "SELECT * FROM user WHERE occupation =",
        "SELECT * FROM user WHERE first_name ="
    ]
    random_query = random.choice(queries)
    return random_query

def unionBased():
    queries = [
        "SELECT first_name FROM user UNION ALL SELECT dob from account where last_name =",
        "SELECT first_name FROM user UNION ALL SELECT last_name from account where occupation =",
        "SELECT first_name FROM user UNION ALL SELECT occupation from account where dob =",
        "SELECT last_name FROM user UNION ALL SELECT dob from account where first_name ="
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