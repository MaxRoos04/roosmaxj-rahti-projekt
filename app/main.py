from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_rooms = [
    { "room_number": 1001, "room_type": "double", "price": 25},
    {"room_number": 1002, "room_type": "single", "price": 10},
    {"room_number": 1003, "room_type": "suite", "price": 250}
]

@app.get("/")
def read_root():
    return { "msg": "Hejsan välommen till hotellbokning"}

@app.get("/rooms")
def rooms():
   return temp_rooms
