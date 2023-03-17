# https://velog.io/@chaeri93/Django-%EA%B8%B0%EC%83%81%EC%B2%AD-%EB%8B%A8%EA%B8%B0%EC%98%88%EB%B3%B4-API-%ED%99%9C%EC%9A%A9%ED%95%98%EA%B8%B0
# import requests # 파이썬 requests 모듈은 간편한 HTTP 요청처리를 위해 사용하는 모듈
import requests # from urllib.request import urlopen, Request # request 쓰면 좀더 안전함.
from urllib.parse import *  # 한글을 URLencode 변환하는 함수. 롯데 --> '%EB%A1%AF%EB%8D%B0'
import json
import ssl
from datetime import *
import math

url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

serviceKey = "s86nUoT8OvF9KjCQEnAYi6kAQ56CU5iiqDHjh384K4gzAVzXj4qFqiCulxZJuhz9yfgwb87yUG%2FCmL1hD5RO%2Bg%3D%3D" # 공공데이터 포털에서 생성된 본인의 서비스 키를 복사 / 붙여넣기
serviceKeyDecoded = unquote(serviceKey, 'UTF-8') # 공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함

now = datetime.now()
today = datetime.today().strftime("%Y%m%d")
y = date.today() - timedelta(days=1)
yesterday = y.strftime("%Y%m%d")
nx = 60 # 위도와 경도를 x,y좌표로 변경
ny = 127
  
if now.minute<45: # base_time와 base_date 구하는 함수
    if now.hour==0:
        base_time = "2330"
        base_date = yesterday
    else:
        pre_hour = now.hour-1
        if pre_hour<10:
            base_time = "0" + str(pre_hour) + "30"
        else:
            base_time = str(pre_hour) + "30"
        base_date = today
else:
    if now.hour < 10:
        base_time = "0" + str(now.hour) + "30"
    else:
        base_time = str(now.hour) + "30"
    base_date = today

<<<<<<< Updated upstream
    
=======


    queryParams = '?' + urlencode({ quote_plus('serviceKey') : serviceKeyDecoded, quote_plus('base_date') : base_date,
                                    quote_plus('base_time') : base_time, quote_plus('nx') : nx, quote_plus('ny') : ny,
                                    quote_plus('dataType') : 'json', quote_plus('numOfRows') : '60'}) #페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다
                                   

    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get('response').get('body').get('items') #데이터들 아이템에 저장
    #print(items)# 테스트

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

NX = 98            ## X축 격자점 수
NY = 76            ## Y축 격자점 수

Re = 6371.00877     ##  지도반경
grid = 5.0          ##  격자간격 (km)
slat1 = 30.0        ##  표준위도 1
slat2 = 60.0        ##  표준위도 2
olon = 129.0        ##  기준점 경도
olat = 35.0         ##  기준점 위도
xo = 210 / grid     ##  기준점 X좌표
yo = 675 / grid     ##  기준점 Y좌표
first = 0

if first == 0 :
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI/ 180.0
    RADDEG = 180.0 / PI


    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD

    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    first = 1

def mapToGrid(lat, lon, code = 0 ):
    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI :
        theta -= 2.0 * PI
    if theta < -PI :
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

def gridToMap(x, y, code = 1):
    x = x - 1
    y = y - 1
    xn = x - xo
    yn = ro - y + yo
    ra = math.sqrt(xn * xn + yn * yn)
    if sn < 0.0 :
        ra = -ra
    alat = math.pow((re * sf / ra), (1.0 / sn))
    alat = 2.0 * math.atan(alat) - PI * 0.5
    if math.fabs(xn) <= 0.0 :
        theta = 0.0
    else :
        if math.fabs(yn) <= 0.0 :
            theta = PI * 0.5
            if xn < 0.0 :
                theta = -theta
        else :
            theta = math.atan2(xn, yn)
    alon = theta / sn + olon
    lat = alat * RADDEG
    lon = alon * RADDEG

    return lat, lon    
>>>>>>> Stashed changes
