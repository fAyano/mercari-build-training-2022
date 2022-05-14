import os
import logging
import pathlib
import json
import sqlite3
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items():
    #---json---
    # filename = 'item.json'
    # js_r = open(filename, 'r')
    # j_data = json.load(js_r)
    # js_r.close()
    # return j_data
    #---------

    #---sqlite3---
    conn = sqlite3.connect('../db/mercari.sqlite3')
    c = conn.cursor()
    sql = 'select * from items'
    c.execute(sql)
    return {"items": c.fetchall()}
    #-------------

@app.post("/items")
def add_item(id: int = Form(...), name: str = Form(...), category: str = Form(...)):
    #---json---
    # filename = 'item.json'
    # js_r = open(filename, 'r')
    # j_data = json.load(js_r)
    # js_r.close()
    # j_add = {'name': name, 'category': category}
    # j_data['items'].append(j_add)
    # js_r = open(filename, 'w')
    # json.dump(j_data, js_r, indent = 2)
    # js_r.close()
    #----------

    #---sqlite3---
    conn = sqlite3.connect('../db/mercari.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO items VALUES (?,?,?)",(id, name, category))
    conn.commit()
    conn.close()
    #-------------

    logger.info(f"Receive item: name -> {name}, category -> {category}")
    return {"message": f"item received: {name}"}

    
@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
