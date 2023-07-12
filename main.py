import psycopg2


def create_db(conn):
    conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS client(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) UNIQUE,
                last_name VARCHAR(40) UNIQUE,
                email VARCHAR(40) UNIQUE
                );
                """)
    conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS phone(
                phone_id SERIAL PRIMARY KEY,
                phone VARCHAR(20) UNIQUE,
                client_id INTEGER NOT NULL REFERENCES client(client_id)
                );
                """)


def add_client(conn, client_id, first_name, last_name, email):
    conn.cursor().execute(""" INSERT INTO client(client_id, first_name, last_name, email) VALUES(%(client_id)s,
    %(first_name)s, %(last_name)s, %(email)s) """, {'client_id': client_id, 'first_name': first_name, 'last_name':
        last_name, 'email': email})


def add_phone(conn, phone_id, phone, client_id):
    conn.cursor().execute("""
                INSERT INTO phone(phone_id, phone, client_id) VALUES(%(phone_id)s, %(phone)s, %(client_id)s);
                """, {'phone_id': phone_id, 'phone': phone, 'client_id': client_id})


def change_client(conn, client_id, **kwargs):
    for key, value in list(kwargs.items()):
        if key == 'first_name':
            conn.cursor().execute("""
                                UPDATE client SET first_name=%(first_name)s WHERE client_id=%(client_id)s;
                                """, {'first_name': value, 'client_id': client_id})
        elif key == 'last_name':
            conn.cursor().execute("""
                                UPDATE client SET last_name=%(last_name)s WHERE client_id=%(client_id)s;
                                """, {'last_name': value, 'client_id': client_id})
        elif key == 'email':
            conn.cursor().execute("""
                                UPDATE client SET email=%(email)s WHERE client_id=%(client_id)s;
                                """, {'email': value, 'client_id': client_id})


def delete_phone(conn, client_id):
    conn.cursor().execute("""
                DELETE FROM phone WHERE client_id=%(client_id)s;
                """, {'client_id': client_id})


def delete_client(conn, client_id):
    conn.cursor().execute("""
                DELETE FROM client WHERE client_id=%(client_id)s CASCADE;
                """, {'client_id': client_id})


def find_client(conn, **kwargs):
    for key, value in list(kwargs.items()):
        if key == 'first_name':
            conn.cursor().execute("""
                       SELECT client_id FROM client WHERE first_name=%(first_name)s;
                       """, {'first_name': value})
        elif key == 'last_name':
            conn.cursor().execute("""
                       SELECT client_id FROM client WHERE last_name=%(last_name)s;
                       """, {'last_name': value})
        elif key == 'email':
            conn.cursor().execute("""
                       SELECT client_id FROM client WHERE email=%(email)s;
                       """, {'email': value})
    print(conn.cursor().fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
    conn.close()
