import requests # 기본적인 URL 모듈로는 안되서 대체
from datetime import *
from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수
from datetime import *
import json

class weather_logic:
        
        def __init__(self) -> None:
            pass

        def checkDate():
            now = datetime()
            print(now)

        def callWeather(base_date):
        # require parameter

        # serviceKey : 인증키
        # numOfRows : 한 페이지 결과 수
        # pageNo : 페이지 번호
        # dataType : 응답자료형식
        # base_date : 발표일자
        # base_time : 발표시각
        # nx : 예보지점 X 좌표
        # ny : 예보지점 Y 좌표

        # 고정값인 페이지 주소 + 특수 키
        
            api_url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
            # 여까지는 일반적인 URL
            # urlencode() url을 인코딩해서 특수문자 변환해줌

            queryString = "?" + urlencode(
                {   

                    'serviceKey' : '6hhxOoRZmduvmq1x2rC8tUpOTEJPythkOXqaCfRhb1G8rL++dNSwoN9DEGcZKHGhumwHaWyhtgGXbNDBbE/J9g==',
                    'pageNo' : '1',
                    'numOfRows' : '1000',
                    'dataType' : 'json', 
                    'base_date' : 'base_date',
                    'base_time' : '0500', 
                    'nx' : '35', 
                    'ny' : '129'
                })

            total_url = api_url + queryString
            # SSL 문제 때문에 계속 에러나서 진행이 안됐음
            response = requests.get(total_url, verify=False)
            json_data = json.loads(response.text)

            items = json_data['response']['body']['items']

            weather_data = dict()

            for item in items['item']:
                # 날짜/시간 확인
                Date = item['fcstDate']
                Time = item['fcstTime']
                if item['fcstDate'] not in weather_data:
                    weather_data[Date] = dict()
                if item['fcstTime'] not in weather_data[Date]:
                    weather_data[Date][Time] = dict()

                # 예보 값
                # 강수확률 (%)
                if item['category'] == 'POP':
                    weather_data[Date][Time]['pop'] = item['fcstValue']
                # 강수형태 
                if item['category'] == 'PTY':
                    weather_data[Date][Time]['pty'] = item['fcstValue']
                # 1시간 강수량
                if item['category'] == 'PCP':
                    weather_data[Date][Time]['pcp'] = item['fcstValue']
                # 습도
                if item['category'] == 'REH':
                    weather_data[Date][Time]['reh'] = item['fcstValue']
                # 1시간 신적설
                if item['category'] == 'SNO':
                    weather_data[Date][Time]['sno'] = item['fcstValue']
                # 하늘상태
                if item['category'] == 'SKY':
                    weather_data[Date][Time]['sky'] = item['fcstValue']
                # 1시간 기온
                if item['category'] == 'TMP':
                    weather_data[Date][Time]['tmp'] = item['fcstValue']
                # 일 최저기온
                if item['category'] == 'TMN':
                    weather_data[Date][Time]['tmn'] = item['fcstValue']
                # 일 최고기온
                if item['category'] == 'TMX':
                    weather_data[Date][Time]['tmx'] = item['fcstValue']
                # 풍속(동서성분)
                if item['category'] == 'UUU':
                    weather_data[Date][Time]['uuu'] = item['fcstValue']
                # 풍속(남북성분)
                if item['category'] == 'VVV':
                    weather_data[Date][Time]['vvv'] = item['fcstValue']
                # 파고
                if item['category'] == 'WAV':
                    weather_data[Date][Time]['wav'] = item['fcstValue']
                # 풍향
                if item['category'] == 'VEC':
                    weather_data[Date][Time]['vec'] = item['fcstValue']
                # 풍속
                if item['category'] == 'WSD':
                    weather_data[Date][Time]['wsd'] = item['fcstValue']
                
            print("response: ", weather_data)

if __name__ == '__main__':
    checkDate()