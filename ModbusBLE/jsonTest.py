import requests
import json

url='http://html.cielpia.com/rskorea/api/test1.php'
jsonstr={'gas': 'CO2', 'figure': 21.00}# dict 타입
jsonstr=json.dumps(jsonstr)#dict 타입에서 str 타입으로 변환
userdata = {"gastiger":jsonstr}
resp = requests.post(url=url, data=userdata)

print(resp.text)