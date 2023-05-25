import psycopg2

#  КАРКАС ДЛЯ КЛАССА:
# Функция, создающая структуру БД (таблицы) - терминал
conn = psycopg2.connect(database="my_db", users="postgres", password="Daha2208")
with conn.cursor() as cur:
    cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) UNIQUE,
            last_name VARCHAR(40) UNIQUE,
            email VARCHAR(40) UNIQUE,
            );
            """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_id(
            phone_id SERIAL PRIMARY KEY,
            phone INTEGER UNIQUE,
            client_id INTEGER NOT NULL REFERENCES client(client_id)
            );
            """)
    conn.commit()  # Фиксируем в БД

    cur.execute("""
            INSERT INTO client(client_id, first_name, last_name, email) VALUES(1, 'Иван', 'Иванов', 
            'ivanov35@gmail.com');
            """)  # Функция, позволяющая добавить нового клиента.
    cur.execute("""
            INSERT INTO phone(phone_id, phone, client_id) VALUES(1, 89093650671, 1);
            """)  # Функция, позволяющая добавить телефон для существующего клиента.
    conn.commit()

    cur.execute("""
            UPDATE client SET email=%s WHERE client_id=%s;
            """, ("ivanov45@gmail.com", 1))
    print(cur.fetchall())  # Функция, позволяющая изменить данные о клиенте.

    cur.execute("""
            DELETE FROM phone WHERE phone_id=%s;  # тут подумать
            """, (1,))
    cur.execute("""
            SELECT * FROM phone;
            """)
    print(cur.fetchall())
    cur.execute("""
            DELETE FROM client WHERE client_id=%s;
            """, (1,))
    cur.execute("""
            SELECT * FROM client;
            """)
    print(cur.fetchall())

    cur.execute("""
           SELECT client_id FROM client WHERE first_name=%s;
           """, ("Иванов",))  # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    print(cur.fetchall())
conn.close()
