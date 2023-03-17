# import requests # 파이썬 requests 모듈은 간편한 HTTP 요청처리를 위해 사용하는 모듈
import requests # from urllib.request import urlopen, Request # request 쓰면 좀더 안전함.
from urllib.parse import *  # 한글을 URLencode 변환하는 함수. 롯데 --> '%EB%A1%AF%EB%8D%B0'
import json
import ssl
from datetime import *

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

    