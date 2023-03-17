import requests
from urllib.parse import *
import json
from datetime import *

# 오늘 전체 날씨 추출 

api_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
querySTR= '?'+urlencode(
{
    'serviceKey' : unquote('4n4Miwzm5p37SLb9Jk9bJa%2FMhFYSTl8mkQIensYxsOuwWyjpePzkk6oyRp3pOsd8GVnzwwQelKHMwSc0bPVfSA%3D%3D'), 
    'pageNo' : '1', 
    'numOfRows' : '700', 
    'dataType' : 'JSON', 
    'base_date' : '20230316', 
    'base_time' : '0600',
    'nx' : '98', 
    'ny' : '76'
}
)


total_url = api_url + querySTR
response = requests.get(total_url)
ls_dict=json.loads(response.text)

ls_response = ls_dict.get('response')

ls_body = ls_response.get('body')

ls_items = ls_body.get('items')
ls_item = ls_items.get('item')


result = {}
result_dict = {}

for item in ls_item:
    result = item
    print(result)
    result_dict.setdefault(result.get('category'), result.get('obsrValue'))


print("부산광역시 연제구 동네예보(초단기실황)데이터")
print("날짜 : "+result.get("baseDate")[:-4]+"년"+result.get("baseDate")[4:-2]+"월"+result.get("baseDate")[6:]+"일"+"시간 : " + result.get("baseTime")[:-2]+"시")
print("강우형태 : "+result_dict["PTY"])
print("습도 : "+result_dict["REH"]+" %")
print("1시간 강수량 : " +result_dict["RN1"]+" mm")
print("기온 : "+result_dict["T1H"] +" ℃")
print("동서바람성분 : " +result_dict["UUU"]+" m/s")
print("남북바람성분 : " + result_dict["VVV"]+" m/s")
print("풍향 : "+result_dict["VEC"])
print("풍속 : "+result_dict["WSD"])