import requests
import json

def check(id, point, expiry, yyyymmddhhmmss):
    token = f'{id}${expiry}${yyyymmddhhmmss}'
    vo = {
        'user_id': id,
        'point': int(point),
        'token': token,
        'memo': '테스트 포인트 차감'
    }

    header = {
        "Content-Type": "application/json; charset=utf-8"
    }

    response = requests.post("http://127.0.0.1:5000/token/check", data=json.dumps(vo), headers=header,
                                timeout=40)
    print(response.content)
    print(response.json())
    return response.json()
