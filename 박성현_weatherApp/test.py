import requests # 기본적인 URL 모듈로는 안되서 대체
from datetime import *
from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수
from datetime import *
import json

API_TIME = [2, 5, 8, 11, 14, 17, 20, 23]
API_MINUTE = 10

class weather_Logic:
        
    def __init__(self) -> None:
        pass

    # API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10

    def Short_term_checkDate(self):
        # 현재 시간
        now = datetime.now()

        for time in range(7):
            if now.hour is API_TIME[time] and now.minute >= API_MINUTE:
                break      
            elif API_TIME[time - 1] < now.hour <= API_TIME[time]:
                return datetime.today().strftime("%Y%m%d") , str(API_TIME[time - 1]) + str(API_MINUTE)
            else:
                time += 1
                
    def Ultra_short_term_checkDate(self):
        # 현재 시간
        now = datetime.now()
        # 포맷 변경
        today = datetime.today().strftime("%Y%m%d")
        # 어제는 오늘 값에 -1
        y = date.today() - timedelta(days=1)
        
        yesterday = y.strftime("%Y%m%d")
        if now.minute < 45: # base_time와 base_date 구하는 함수
            if now.hour == 0:
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
        return base_date, base_time


    def callWeather(self, base_date, base_time):
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
                'base_date' : base_date,
                'base_time' : base_time, 
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
class db_Logic:
    def __init__(self) -> None:
        pass

def main():
    weatherlogic = weather_Logic()
    ctime, dtime = weatherlogic.Short_term_checkDate()
    weatherlogic.callWeather(ctime, dtime)









if __name__ == '__main__':
    main()