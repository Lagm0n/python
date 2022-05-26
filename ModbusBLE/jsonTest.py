import requests
import json
jlist=list()
url='https://html.cielpia.com/rskorea/api/test2.php'
# jsonstr={'gas': 'CO2', 'figure': '21.00','unit':'ppm'}, {'gas': 'CO', 'figure': '21.00','unit':'ppb'}# dict 타입
for i in range(5):
    jsonstr={'gas': '{0}'.format(i+1), 'figure':'{0}'.format(i+9), 'unit':'{0}'.format(i)}
    jlist.append(jsonstr)
print(type(jlist))
print(jlist)
# jsonstr=json.dumps(jsonstr)#dict 타입에서 str 타입으로 변환
jsonstr=json.dumps(jlist)#dict 타입에서 str 타입으로 변환
print(type(jsonstr))
print(jsonstr)


userdata = {"gastiger":jsonstr}
print(userdata)
resp = requests.post(url=url, data=userdata)

print(resp.text)