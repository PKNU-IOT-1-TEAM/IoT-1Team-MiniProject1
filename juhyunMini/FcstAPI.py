# 기상 API 받아서 DB에 업데이트
# API
from urllib.parse import urlencode
from datetime import datetime as dt
import requests


# 기상API
class FcstAPI:
    def __init__(self) -> None:
        print(f'[{dt.now()}] 기상 API 생성')

    # FcstAPI 호출 함수
    def getDataPortalSearch(self, baseDate, baseTime):
        api_url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        queryString = '?' + urlencode(
            {
                'serviceKey': 'Hp7RL4tCw0cXBMTYsWCTrydbix/qtqe4+u5yRNze4LKbniVQhVKmNWMk8IxYObz6/EB41Vo47zCdEVUVRfAvsA==',
                'pageNo': '1',
                'numOfRows': '1000',
                'dataType': 'JSON',
                'base_date': baseDate,
                'base_time': baseTime,
                'nx': 98,
                'ny': 76
            }
        )
        total_url = api_url + queryString
        response = requests.get(total_url, verify=False)
        return response.text

