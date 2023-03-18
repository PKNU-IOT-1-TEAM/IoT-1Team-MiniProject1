import requests # 기본적인 URL 모듈로는 안되서 대체
import pandas as pd
import json
import pymysql 
import urllib3
from datetime import *
from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수
from mysql.connector import *

CODE_INFO = ['POP', 'PTY', 'PCP', 'REH', 'SNO', 'SKY', 'TMP', 'TMN', 'TMX', 'UUU', 'VVV', 'WAV', 'VEC', 'WSD']
API_TIME = [2, 5, 8, 11, 14, 17, 20, 23]
API_MINUTE = 10

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class weather_Logic:
        
    def __init__(self) -> None:
        pass
    # API 제공 시간(~이후) : 02:10, 05:10, 08:10, 11:10, 14:10, 17:10, 20:10, 23:10

    # 단기 예보 함수
    # 현재 시간에 따라 봐야하는 시간대를 구분해서
    # 카테고리 리스트 및 데이터 값 리스트 생성
    def Short_term_checkDate(self):
        # 현재 시간
        now = datetime.now() # 오늘 시간
        today = datetime.today().strftime("%Y%m%d") # 특수문자 제거
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
        day_after_tomorrow = (date.today() - timedelta(days=2)).strftime("%Y%m%d")

        for time in range(8):
            now_time = str(API_TIME[time]) + str(API_MINUTE) # 현재와 제일 가까운 시간
            pre_time = str(API_TIME[time - 1]) + str(API_MINUTE) # 이전 시간 - 발표 시간 시간 사이에 끼어있는 애매한 시간
            y_time = str(API_TIME[7]) + str(API_MINUTE)
            
            if now.hour is API_TIME[time] and now.minute >= API_MINUTE:
                base_date = today
                base_time = now_time
                break
            elif API_TIME[time - 1] < now.hour <= API_TIME[time]:
                base_date = today
                base_time = pre_time
                break
            elif now.hour < API_TIME[0]:
                base_date = yesterday
                base_time = y_time
                break
            else:
                time += 1

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

        ITEM = json_data['response']['body']['items']['item']

        list_data = []
        list_info = []

        for i in range(len(ITEM)):

            list_info_data = []

            for j in range(len(CODE_INFO)):
                if ITEM[i]['category'] == str(CODE_INFO[j]):
                    list_info_data.append(ITEM[i]['category'])
                    list_info_data.append(ITEM[i]['fcstDate'])
                    list_info_data.append(ITEM[i]['fcstTime'])
                    list_data.append(ITEM[i]['fcstValue'])
                else:
                    j += 1
            list_info.append(list_info_data)
            i += 1

        return list_info, list_data

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
    # 리스트로 바뀐 데이터 데이터 베이스에 올려주는 함수    
    def db_data_weather(self, list_info, list_data):

        conn = pymysql.connect(
            host = '127.0.0.1', 	 #ex) '127.0.0.1' "210.119.12.66"
            port = 3306,
            user = "root", 		 #ex) root
            password = "12345",
            database = "miniproject01", 
            charset = 'utf8'
        )
        # Cursor Object 가져오기
        cur = conn.cursor()

        query = '''DELETE FROM weather'''
        cur.execute(query)

        for fcstData in list_info:
            if 'TMN' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, POP, PCP, REH, SNO, TMN)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
                                fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
                                fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN']))
            elif 'TMM' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, POP, PCP, REH, SNO, TMM)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
                                fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
                                fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMM']))
            else:
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD,  SKY, POP, PCP, REH, SNO)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
                                fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
                                fcstData['PCP'], fcstData['REH'], fcstData['SNO']))
                
        conn.commit()

        conn.close()
        print('저장')

def main():
    weatherlogic = weather_Logic()
    list_info, list_data = weatherlogic.Short_term_checkDate()
    print(list_info)
    print('------------------------------------')
    print(list_data)
if __name__ == '__main__':
    main()