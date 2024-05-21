from typing import Union

from fastapi import FastAPI

app = FastAPI()

import requests, json, os

is_koyeb = False

if not is_koyeb:
##############################
# 下面为 .env 文件模式读取变量
    from dotenv import load_dotenv
# 加载 .env 文件
    load_dotenv()
##############################

model="gemini-1.5-pro-latest"
entrypoint="https://generativelanguage.googleapis.com/v1beta"
if is_koyeb:
    apikey = os.environ.get('apikey') # 读取环境变量 koyeb 环境变量模式
else:
    apikey = os.getenv('apikey') # 读取环境变量 .env 模式
url=f'{entrypoint}/models/{model}:generateContent?key={apikey}'
headers = {'Content-Type': 'application/json'}

@app.get("/")
def read_root():
    return {"Hello": "World"}

    # data = {
    #     'contents': [
    #         {
    #             'parts': [
    #                 {
    #                     'text': '你好'
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
 
    # response = requests.post(url, headers=headers, data=json.dumps(data))
    # return response.json()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/sendtext/{text}")
def read_item(text: str):
    return send_text(text)

def send_text(text):
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': text
                        }
                    ]
                }
            ]
        }
    return data
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()  
