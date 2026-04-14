import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(
        DATABASE_URL,
        autocommit=True,
        row_factory=psycopg.rows.dict_row
    )

def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS guests (
                id SERIAL PRIMARY KEY,
                firstname VARCHAR(100) NOT NULL,
                lastname VARCHAR(100) NOT NULL,
                address VARCHAR(255)
            );

            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                room_number INT NOT NULL,
                type VARCHAR(50) NOT NULL,
                price NUMERIC(10,2) NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                guest_id INT NOT NULL,
                room_id INT NOT NULL,
                datefrom DATE NOT NULL,
                dateto DATE NOT NULL,
                addinfo VARCHAR(255),
                FOREIGN KEY (guest_id) REFERENCES guests(id),
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            );
        """)