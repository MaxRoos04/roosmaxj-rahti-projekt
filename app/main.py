from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Hellow fellow student! HaHaHA", "v": "0.1" }


@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}


from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/api/ip")
async def get_ip(request: Request):
    return {"ip": request.client.host}