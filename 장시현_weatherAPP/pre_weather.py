import requests
from urllib.parse import *
import json
from datetime import *


# 실시간 정보 추출 

api_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
service_key = '4n4Miwzm5p37SLb9Jk9bJa/MhFYSTl8mkQIensYxsOuwWyjpePzkk6oyRp3pOsd8GVnzwwQelKHMwSc0bPVfSA=='
serviceKeyDecoded = unquote(service_key, 'UTF-8')


now = datetime.now()
today= datetime.today().strftime('%Y%m%d')
y = date.today()-timedelta(days=1)
yesterday = y.strftime('%Y%m%d')
nx = 98
ny = 76

if now.minute < 45:
    if now.hour == 0:
        base_time ='2330'
        base_data = yesterday   
    else :
        pre_hour = now.hour -1
        if pre_hour < 10:
            base_time = '0' + str(pre_hour) +'30'
        else:
            base_time = str(pre_hour) +'30'
        base_data = today
else:
    if now.hour < 10:
        base_time= '0'+ str(now.hour)+'30'
    else:
        base_time  = str(now.hour) +'30'
    base_data = today


queryParams = '?' + urlencode({ quote_plus('serviceKey') : serviceKeyDecoded, quote_plus('base_date') : base_data,
                                quote_plus('base_time') : base_time, quote_plus('nx') : nx, quote_plus('ny') : ny,
                                quote_plus('dataType') : 'json', quote_plus('numOfRows') : '60'}) #페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다
                                   

# 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
res = requests.get(api_url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
items = res.json().get('response').get('body').get('items') #데이터들 아이템에 저장
# print(items)# 테스트

weather_data = dict()

for item in items['item']:
    # 기온
    if item['category'] == 'T1H':
        weather_data['tmp'] = item['fcstValue']
    # 습도
    if item['category'] == 'REH':
        weather_data['hum'] = item['fcstValue']
    # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
    if item['category'] == 'SKY':
        weather_data['sky'] = item['fcstValue']
    # 1시간 동안 강수량
    if item['category'] == 'RN1':
        weather_data['rain'] = item['fcstValue']

print("response: ", weather_data)    

