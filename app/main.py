from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
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

#Skapa databas schema
create_schema()

temp_rooms = [
    { "room_number": 1001, "room_type": "double", "price": 25},
    {"room_number": 1002, "room_type": "single", "price": 10},
    {"room_number": 1003, "room_type": "suite", "price": 250}
]

@app.get("/")
def read_root():
    #testar databasen 
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 'Databasen fungerar' as msg, version() as version
        """)
        db_status = cur.fetchone()
    return { "msg": "Hejsan välommen till hotellbokning", "db": db_status}

@app.get("/rooms")
def rooms():
   return temp_rooms

@app.post("/bookings")
def create_booking():
    return{ "msg": "Bokning skapad!"}