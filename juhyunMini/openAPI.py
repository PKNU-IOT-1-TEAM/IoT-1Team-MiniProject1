from urllib.parse import quote, unquote, urlencode  # 한글을 URLencode 변환하는 함수
import requests
import json

# 실시간 하천 수위 조회
def getDataPortalSearch(type):
    api_url = 'http://apis.data.go.kr/6260000/BusanRvrwtLevelInfoService/getRvrwtLevelInfo'
    queryString = '?' + urlencode(
        {
            'serviceKey': 'Hp7RL4tCw0cXBMTYsWCTrydbix/qtqe4+u5yRNze4LKbniVQhVKmNWMk8IxYObz6/EB41Vo47zCdEVUVRfAvsA==',
            'pageNo': '1',
            'numOfRows':'100',
            'resultType': type
        }
    )

    total_url = api_url + queryString
    response = requests.get(total_url, verify=False)
    return response.text  

try:
    result = getDataPortalSearch('json')
    # print(result)
    json_data = json.loads(result)  # 딕셔너리
    water_data = json_data['getRvrwtLevelInfo']['body']['items']['item']    # 리스트
    for item in water_data:
        print(item)     # 딕셔너리
except Exception as e:
    print('찾는 데이터가 없습니다.')