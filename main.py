import psycopg2


def create_db(conn):
    conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) UNIQUE,
            last_name VARCHAR(40) UNIQUE,
            email VARCHAR(40) UNIQUE,
            );
            """)
    conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS phone_id(
            phone_id SERIAL PRIMARY KEY,
            phone INTEGER UNIQUE,
            client_id INTEGER NOT NULL REFERENCES client(client_id)
            );
            """)


def add_client(conn, client_id, first_name, last_name, email):
    conn.cursor().execute(f"""
            INSERT INTO client(client_id, first_name, last_name, email) VALUES({client_id}, {first_name}, {last_name}, 
            {email});
            """)


def add_phone(conn, phone_id, phone, client_id):
    conn.cursor().execute(f"""
                INSERT INTO phone(phone_id, phone, client_id) VALUES({phone_id}, {phone}, {client_id});
                """)


def change_client(conn, client_id, first_name):
    conn.cursor().execute(f"""
                UPDATE client SET first_name=%s WHERE client_id=%s;
                """, ({client_id}, {first_name}))
    print(conn.cursor().fetchall())


def delete_phone(conn, client_id):
    conn.cursor().execute("""
                DELETE FROM phone WHERE client_id=%s;
                """, (client_id,))


def delete_client(conn, client_id):
    conn.cursor().execute("""
                DELETE FROM client WHERE client_id=%s;
                """, (client_id,))


def find_client(conn, last_name):
    conn.cursor().execute("""
               SELECT client_id FROM client WHERE last_name=%s;
               """, (last_name,))
    print(conn.cursor().fetchall())


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    print(conn.create_db())
    print(conn.add_client(1, "Иван", "Иванов", "ivan123@gmail.com"))
    print(conn.add_phone(1, 89092377762, 1))
    print(conn.change_client(1, "Костя"))
    print(conn.delete_phone(1))
    print(conn.delete_client(1))
    print(conn.find_client("Иванов"))

conn.close()
