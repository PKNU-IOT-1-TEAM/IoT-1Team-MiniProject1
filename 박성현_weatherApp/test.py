import requests # 기본적인 URL 모듈로는 안되서 대체
from datetime import *
from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수
import json

# 고정값인 페이지 주소 + 특수 키
api_url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
# 여까지는 일반적인 URL
queryString = "?" + urlencode(
    {   
        # url을 인코딩해서 특수문자 변환해줌
        'serviceKey' : '6hhxOoRZmduvmq1x2rC8tUpOTEJPythkOXqaCfRhb1G8rL++dNSwoN9DEGcZKHGhumwHaWyhtgGXbNDBbE/J9g==',
        'pageNo' : '1',
        'numOfRows' : '1000',
        'dataType' : 'json', 
        'base_date' : '20230315',
        'base_time' : '0500', 
        'nx' : '35', 
        'ny' : '129'
    })
total_url = api_url + queryString
# SSL 문제 때문에 계속 에러나서 진행이 안됐음
response = requests.get(total_url, verify=False)
json_data = json.loads(response.text)

weather_data = json_data['response']['body']['items']['item']

print(weather_data)