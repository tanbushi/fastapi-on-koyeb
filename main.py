from typing import Union

from fastapi import FastAPI

app = FastAPI()

import requests


@app.get("/")
def read_root():
    x = requests.get('https://www.runoob.com/')
    return {"Hello": x.text}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

    
