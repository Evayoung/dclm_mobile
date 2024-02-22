import requests
import sqlite3
import json

url = ""


def set_server_url(data):
    global url  # Use the global keyword to modify the global variable
    url = data


def get_count(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    return headers


def create_user(data):
    """ Make request to the server api to create user """
    error = "IntegrityError('(psycopg2.errors.UniqueViolation)"
    end_point = f"{url}/users/"
    response = requests.post(end_point, json=data)
    return response


def get_details(data):
    """ Make call to the API for the last user, create new user id and send back the id to the current user """
    end_point = f"{url}/workers/{data}"

    response = requests.get(end_point, json=data)

    return response


def login_user(payload):
    end_point = f"{url}/login/"
    response = requests.post(end_point, data=payload)

    return response


def create_counts(payload, token):
    end_point = f"{url}/counts/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    response = requests.post(end_point, headers=headers, data=payload_json)

    return response


def get_workers(token, a, b, c, d):
    end_point = f"{url}/workers/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "get_all": a,  # To get all workers
        "location_id": b,
        "gender": c,
        "unit": d
    }

    response = requests.get(end_point, headers=headers, params=params)
    return response


def submit_worker_attendance(payload, token):
    end_point = f"{url}/attendance/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload_json = json.dumps(payload)

    response = requests.post(end_point, headers=headers, data=payload_json)

    return response


def create_online_con_record(payload, token):
    end_point = f"{url}/record/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload_json = json.dumps(payload)

    response = requests.post(end_point, headers=headers, data=payload_json)

    return response


def generate_worker_id(payload):
    """ This make request to the server to generate the worker's ID """
    end_point = f"{url}/workers/generate_id"

    payload_json = json.dumps(payload)

    response = requests.post(end_point, data=payload_json)

    return response


def create_new_worker(payload):
    """ This make a post request to the server to submit the workers data for registration """
    end_point = f"{url}/workers/"

    payload_json = json.dumps(payload)

    response = requests.post(end_point, data=payload_json)

    return response


# ####################################################################################################################
#                                           OFFLINE DATABASE
# ####################################################################################################################
# Create a connection to the database (or create a new one if it doesn't exist)
conn = sqlite3.connect('database/workers.db')


# Create a cursor object to interact with the database

# ############################################### CREATE FUNCTION ###################################################

# Create a table to store worker details
def create_worker():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY,
            user_id TEXT UNIQUE,
            location_id TEXT,
            location TEXT,
            name TEXT,
            gender TEXT,
            phone TEXT,
            email TEXT,
            unit TEXT
        )
    ''')
    conn.commit()


def create_attendance():
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                program_domain TEXT,
                program_type TEXT,
                location TEXT,
                location_id TEXT,
                date TEXT,
                worker_id TEXT UNIQUE,
                name TEXT,
                gender TEXT,
                contact TEXT,
                email TEXT,
                unit TEXT,
                church_id TEXT,
                local_church TEXT,
                status TEXT
            )
        ''')
        conn.commit()
    except Exception as e:
        print(e)


def create_offline_count():
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS counter(
        id INTEGER PRIMARY KEY,
        program_domain TEXT,
        program_type TEXT,
        location TEXT,
        location_id TEXT,
        date TEXT,
        adult_male TEXT,
        adult_female TEXT,
        youth_male TEXT,
        youth_female TEXT,
        boys TEXT,
        girls TEXT,
        total TEXT,
        author TEXT
        )
        """)
    conn.commit()


def create_offline_convert():
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS record(
        id INTEGER PRIMARY KEY,
        program_domain TEXT,
        program_type TEXT,
        location TEXT,
        location_id TEXT,
        date TEXT,
        reg_type TEXT,
        name TEXT,
        gender TEXT,
        phone TEXT,
        home_address TEXT,
        marital_status TEXT,
        social_group TEXT,
        social_status TEXT,
        status_address TEXT,
        level TEXT,
        salvation_type TEXT,
        invited_by TEXT,
        author TEXT
        )
    """)
    conn.commit()


def create_user_log():
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id TEXT UNIQUE,
        name TEXT,
        email TEXT,
        role TEXT
        )
    """)

    conn.commit()


def create_attendance_count():
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_taken(
        id INTEGER PRIMARY KEY,
        worker_id TEXT UNIQUE
        )
    """)

    conn.commit()


def create_program_setup():
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS setup(
        id INTEGER PRIMARY KEY,
        program_domain TEXT UNIQUE,
        program_type TEXT,
        program_level TEXT,
        program_location TEXT
        )
    """)

    conn.commit()


# ################################################# INSERT FUNCTION ##############################################

def insert_attendance_count(worker_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO attendance_taken (worker_id) VALUES(?)
        """, (worker_id,))
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        return False


def insert_setup(program_domain, program_type, program_level, program_location):
    """ this collect the setup data for data submissions """
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO setup (program_domain, program_type, program_level, program_location) 
        VALUES( ?, ?, ?, ?)
        """, (program_domain, program_type, program_level, program_location,))
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        return False


def insert_offline_count(payload):
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO counter (program_domain, program_type, location, location_id, date, adult_male,
        adult_female, youth_male, youth_female, boys, girls, total, author) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (payload['program_domain'], payload['program_type'], payload['location'], payload['location_id'],
              payload['date'], payload['adult_male'], payload['adult_female'], payload['youth_male'],
              payload['youth_female'], payload['boys'], payload['girls'], payload['total'], payload['author']))

        conn.commit()

        return True

    except Exception as e:
        conn.rollback()
        return False


def insert_user(payload):
    cursor = conn.cursor()
    try:
        # Insert a new worker's details into the table, ignoring if user_id already exists
        cursor.execute('''
                INSERT OR IGNORE INTO users (
                user_id, name, email, role
                ) VALUES (?, ?, ?, ?)
            ''', (payload['user_id'], payload['user_name'], payload['user_email'], payload['user_role']))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()  # Rollback transaction if user_id already exists


def insert_convert_offline(program_domain, program_type, location, location_id, date, reg_type, name, gender, phone,
                           home_address, marital_status, social_group, social_status, status_address, level,
                           salvation_type, invited_by, author):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO record (program_domain, program_type, location, location_id, date, reg_type, name, 
            gender, phone, home_address, marital_status, social_group, social_status, status_address, level, 
            salvation_type, invited_by, author) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (program_domain, program_type, location, location_id, date, reg_type, name, gender, phone,
                  home_address, marital_status, social_group, social_status, status_address, level, salvation_type,
                  invited_by, author))

        conn.commit()

    except Exception as e:
        print(e)


def insert_attendance(payload):
    cursor = conn.cursor()
    try:
        cursor.execute('''
                INSERT OR IGNORE INTO attendance (program_domain, program_type, location, location_id, date, worker_id, 
                name, gender, contact, email, unit, church_id, local_church, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (payload['program_domain'], payload['program_type'], payload['location'], payload['location_id'],
                  payload['date'], payload['worker_id'], payload['name'], payload['gender'], payload['contact'],
                  payload['email'], payload['unit'], payload['church_id'], payload['local_church'], payload['status']))

        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
        conn.rollback()


def insert_worker(user_id, location_id, location, name, gender, phone, email, unit):
    print("i was here")
    print(user_id, location_id, location, name, gender, phone, email, unit)
    cursor = conn.cursor()
    try:
        # Insert a new worker's details into the table, ignoring if user_id already exists
        cursor.execute('''
                INSERT OR IGNORE INTO workers (
                    user_id, location_id, location, name, gender, phone, email, unit
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, location_id, location, name, gender, phone, email, unit))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()  # Rollback transaction if user_id already


# ############################################# UPDATE FUNCTION ######################################################

def update_attendance(program_domain, program_type, location, location_id, date, status, worker_id):
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE attendance SET program_domain = ?, program_type = ?, location = ?, 
                        location_id = ?, date = ?, status = ? 
                        WHERE worker_id = ?''',
                       (program_domain, program_type, location, location_id, date, status, worker_id))

        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


# ############################################# SELECT FUNCTION ######################################################

def search_workers_by_params(location_id=None,
                             location=None,
                             units=None,
                             user_id=None,
                             name=None,
                             phone=None,
                             email=None,
                             get_all=None):
    cursor = conn.cursor()
    try:
        if get_all:
            query = cursor.execute("SELECT * FROM attendance").fetchall()
            return query
        # Construct the base query to fetch workers
        query = 'SELECT * FROM attendance WHERE 1=1'

        # Add conditions based on parameters
        if location:
            query += ' AND location LIKE ?'

        if units:
            query += ' AND unit LIKE ?'

        if user_id:
            query += ' AND user_id = ?'

        if phone:
            query += ' AND phone = ?'

        if email:
            query += ' AND email = ?'

        # Execute query with parameters
        if name:
            # Use LIKE to search for a word within a parameter using % wildcard
            cursor.execute(f"{query} AND name LIKE ?", ('%' + name + '%',), )
        else:
            cursor.execute(query, (user_id, ('%' + location_id + '%',), ('%' + location + '%',),
                                   ('%' + units + '%',), phone, email))

        # Fetch and return the results
        results = cursor.fetchall()
        return results

    except Exception as e:
        query = cursor.execute("SELECT * FROM attendance").fetchall()

        return query


def fetch_details(id_):
    cursor = conn.cursor()
    if id_:
        query = cursor.execute("""SELECT * FROM attendance WHERE worker_id = ?""", (id_,)).fetchone()
        return query


def commit_and_close():
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def select_all_attendance():
    cursor = conn.cursor()
    query = cursor.execute("SELECT * FROM attendance").fetchall()
    return query


def offline_login(payload):
    cursor = conn.cursor()
    print(payload['username'])
    query = cursor.execute("""SELECT * FROM users WHERE email = ?""",
                           (payload['username'],)).fetchone()
    return query


def get_counts():
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM counter""").fetchall()
    return data


def get_registration():
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM record""").fetchall()
    return data


def fetch_setup(id_):
    cursor = conn.cursor()
    query = cursor.execute("""SELECT * FROM setup """).fetchall()
    return query


def fetch_attendance_count():
    cursor = conn.cursor()
    query = cursor.execute("""SELECT worker_id FROM attendance_taken """).fetchall()
    return query


def select_each_count(id_):
    cursor = conn.cursor()
    response = cursor.execute("SELECT * FROM counter WHERE id = ?", (id_,)).fetchone()
    return response


def select_each_reg(id_):
    cursor = conn.cursor()
    response = cursor.execute("SELECT * FROM record WHERE id = ?", (id_,)).fetchone()
    return response


# ################################################ DELETE FUNCTION ###############################################


def delete_registration(id_):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM record WHERE id = ?", (id_,))
    conn.commit()
    return True


def delete_all_attendance():
    cursor = conn.cursor()
    try:
        query = cursor.execute("DELETE FROM attendance")
        conn.commit()
        return "Successful!"
    except Exception as e:
        return str(e)


def delete_one_attendance(user_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance WHERE worker_id = ?", (user_id,))
    conn.commit()
    return True


def delete_counts(id_):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM counter WHERE id = ?", (id_,))
        conn.commit()
        return True
    except Exception as e:
        print(e)


def delete_all_taken_attendance():
    cursor = conn.cursor()
    try:
        query = cursor.execute("DELETE FROM attendance_taken")
        conn.commit()
    except Exception as e:
        return str(e)


def delete_setup():
    cursor = conn.cursor()
    try:
        query = cursor.execute("DELETE FROM setup")
        conn.commit()
    except Exception as e:
        return str(e)


def delete_an_attendance(worker_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance_taken WHERE worker_id = ?", (worker_id,))
    conn.commit()
    return True
