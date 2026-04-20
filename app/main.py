from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from app.db import get_conn, create_schema

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables at startup
create_schema()

# Pydantic model
class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT version()")
        result = cur.fetchone()
    return {"msg": "Hotel API!", "db_status": result}

# List all rooms
@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM rooms
            ORDER BY room_number
        """)
        rooms = cur.fetchall()
    return rooms

# Get one room
@app.get("/rooms/{id}")
def get_room(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM rooms
            WHERE id = %s
        """, [id])
        room = cur.fetchone()
    return room

# Create booking
@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bookings (
                guest_id,
                room_id,
                datefrom,
                dateto
            ) VALUES (
                %s, %s, %s, %s
            ) RETURNING id
        """, (
            booking.guest_id,
            booking.room_id,
            booking.datefrom,
            booking.dateto
        ))
        new_booking = cur.fetchone()
    return {"msg": "Booking created!", "id": new_booking["id"]}

#Endpoint 
@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 
                b.id,
                g.firstname,
                g.lastname,
                r.room_number,
                b.datefrom,
                b.dateto,
                (b.dateto - b.datefrom) AS nights,
                ((b.dateto - b.datefrom) * r.price) AS total_price
            FROM bookings b
            INNER JOIN guests g ON b.guest_id = g.id
            INNER JOIN rooms r ON b.room_id = r.id
            ORDER BY b.datefrom DESC
        """)
        bookings = cur.fetchall()
    return bookings


@app.get("/guests")
def get_guests():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 
                g.id,
                g.firstname,
                g.lastname,
                g.created_at,
                (
                    SELECT COUNT(*) 
                    FROM bookings b 
                    WHERE b.guest_id = g.id
                ) AS visits
            FROM guests g
            ORDER BY g.lastname
        """)
        guests = cur.fetchall()
    return guests

