import requests # 기본적인 URL 모듈로는 안되서 대체
import pandas as pd
import json
import pymysql 
import urllib3
from datetime import *
from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수
from mysql.connector import *

CODE_INFO = ['POP', 'PTY', 'PCP', 'REH', 'SNO', 'SKY', 'TMP', 'TMN', 'TMM', 'UUU', 'VVV', 'WAV', 'VEC', 'WSD']
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
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y%m%d") # 어제 날짜

        for time in range(len(API_TIME)):
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

        # 고정값인 페이지 주소 + 특수 키

        api_url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        # 여까지는 일반적인 URL
        # urlencode() url을 인코딩해서 특수문자 변환해줌

        queryString = "?" + urlencode(
            {   
                # require parameter
                'serviceKey' : '6hhxOoRZmduvmq1x2rC8tUpOTEJPythkOXqaCfRhb1G8rL++dNSwoN9DEGcZKHGhumwHaWyhtgGXbNDBbE/J9g==',# serviceKey : 인증키
                'pageNo' : '1', # pageNo : 페이지 번호
                'numOfRows' : '1000', # numOfRows : 한 페이지 결과 수
                'dataType' : 'json', # dataType : 응답자료형식
                'base_date' : base_date, # base_date : 발표일자
                'base_time' : base_time, # base_time : 발표시각
                'nx' : '35', # nx : 예보지점 X 좌표
                'ny' : '129' # ny : 예보지점 Y 좌표
            })

        total_url = api_url + queryString
        # SSL 문제 때문에 계속 에러나서 진행이 안됐음
        response = requests.get(total_url, verify=False)
        json_data = json.loads(response.text)

        ITEM = json_data['response']['body']['items']['item']

        list_data = []
        list_info = []  # 2차원 배열
        # 2차원 배열로 단기예보 항목명, 날짜, 시간 별로 구분
        for i in range(len(ITEM)):
            list_info_data = [] # 1차원 배열
            for j in range(len(CODE_INFO)):
                # 정해진 순서대로 카테고리 값이 같다면
                if ITEM[i]['category'] == str(CODE_INFO[j]):
                    # 2차원 배열에 카테고리, 날짜, 시간 추가
                    list_info_data.append(ITEM[i]['category'])
                    list_info_data.append(ITEM[i]['fcstDate'])
                    list_info_data.append(ITEM[i]['fcstTime'])
                    # 데이터 값 리스트에 저장
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
        list_data_num = 0

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
        # 쿼리 초기화(임시)
        query = '''DELETE FROM weather'''
        cur.execute(query)
        # DB 불러오기

        # 데이터 갯수만큼 돌면서 날짜, 시간, 데이터 형태 읽고 DB에 등록
        for item in range(len(CODE_INFO)):
            get_index_result = f'SELECT fcstDate, fcstTime, {CODE_INFO[item]} FROM weather'
            set_index_result = f'INSERT INTO weather (fcstDate, fcstTime, {CODE_INFO[item]}) VALUES ({list_info[0][1]}, {list_info[0][2]}, {list_data[list_data_num]})'
            set_index_date_result = f'INSERT INTO weather (fcstTime, {CODE_INFO[item]}) VALUES ({list_info[0][2]}, {list_data[list_data_num]})'
            update_index_result = f'UPDATE weather SET {CODE_INFO[item]} = ({list_data[list_data_num]})'
            
            cur.execute(get_index_result)
            row = cur.fetchall()
            print(row)

            try:
                if row == ():
                    cur.execute(set_index_result)
                    list_data_num += 1
                elif row['fcstDate'] == '' and row['fcstTime'] == '':
                    cur.execute(set_index_result)
                    list_data_num += 1
                elif row['fcstDate'] != '' and row['fcstTime'] == '':
                    cur.execute(set_index_date_result)
                    list_data_num += 1
                elif row['fcstDate'] != '' and row['fcstTime'] != '' and row[f'{CODE_INFO[item]}'] == '':
                    cur.execute(update_index_result)
                    list_data_num += 1

            except Exception as e:
                print(e)

        conn.commit()

        # 결과 가져오기
        print(cur.fetchall())
        conn.close()
        print('저장')

def main():
    weatherlogic = weather_Logic()
    list_info, list_data = weatherlogic.Short_term_checkDate()
    weatherlogic.db_data_weather(list_info, list_data)

if __name__ == '__main__':
    main()