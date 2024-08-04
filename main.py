from typing import Union

from fastapi import FastAPI

app = FastAPI()

import requests, json, os

is_koyeb = True

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

@app.post("/questions/")
def create_question(question:dict):
    # return url
    response = requests.post(url, headers=headers, data=json.dumps(question))
    response_json = response.json()
    return response_json['candidates'][0]['content']['parts'][0]['text']

@app.get("/")
def read_root():
    print('909090909090909')
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

@app.post("/items/")
def create_item(item:dict):
    try:
        q=item['q']
    except:
        return "q not found"
    return send_text(q)

@app.post("/v1/completions")
def create_completion(data:dict):
    try:
        # 准备数据
        data_str = json.dumps(data)    
        
        # 发送请求
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # 检查响应状态码
        response.raise_for_status()

        # 解析响应
        response_json = response.json()
        
        # 安全地访问响应内容
        candidates = response_json.get('candidates', [])
        if candidates:
            content = candidates[0].get('content', {})
            parts = content.get('parts', [])
            if parts:
                return parts[0].get('text', "")
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except KeyError as e:
        print(f"解析响应失败: 缺少必要的键 {e}")
    except Exception as e:
        print(f"未知错误: {e}")

    return None  # 出现异常时返回None

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
    # response = {"candidates":[{"content":{"parts":[{"text":"你好呀！ 很高兴见到你！ 你想聊些什么呢？ \n"}],"role":"model"},"finishReason":"STOP","index":0,"safetyRatings":[{"category":"HARM_CATEGORY_SEXUALLY_EXPLICIT","probability":"NEGLIGIBLE"},{"category":"HARM_CATEGORY_HATE_SPEECH","probability":"NEGLIGIBLE"},{"category":"HARM_CATEGORY_HARASSMENT","probability":"NEGLIGIBLE"},{"category":"HARM_CATEGORY_DANGEROUS_CONTENT","probability":"NEGLIGIBLE"}]}],"usageMetadata":{"promptTokenCount":2,"candidatesTokenCount":15,"totalTokenCount":17}}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
    # return response_json['candidates'][0]['content']['parts'][0]['text'] 


