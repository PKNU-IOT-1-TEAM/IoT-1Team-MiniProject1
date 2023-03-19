import requests # 기본적인 URL 모듈로는 안되서 대체
import json
import pymysql 
import urllib3
import sys
from datetime import *
from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수
from mysql.connector import *


CODE_INFO = ['TMP','UUU','VVV','VEC','WSD','SKY','PTY','POP','WAV','PCP','REH','SNO','TMN', 'TMX'  ]
API_TIME = [2, 5, 8, 11, 14, 17, 20, 23]
API_MINUTE = 10

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 단기 예보 API 불러오기 및 DB업로드 클래스
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
                if now.hour < 10:
                    base_date = today
                    base_time = '0' + now_time
                    break
                else:
                    base_date = today
                    base_time = now_time
                    break
            elif API_TIME[time - 1] < now.hour <= API_TIME[time]:
                if now.hour < 10:
                    base_date = today
                    base_time = '0' + pre_time
                    break 
                else:
                    base_date = today
                    base_time = '0' + pre_time
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

        list_data = []  # 1차원 배열
        list_data_detail = []  # 2차원 배열
        # 2차원 배열로 단기예보 항목명, 날짜, 시간 별로 구분
        code_num = 0
        list_data_num = 0

        # DB 연결
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
        query = '''DELETE FROM `miniproject01`.`weather`'''
        cur.execute(query)
        get_index_result = f'SELECT * FROM weather;'
        cur.execute(get_index_result)
        
        set_TMP_result = f'INSERT INTO weather (fcstDate, fcstTime, TMP, UUU, VVV, VEC, WSD, SKY, PTY, POP, WAV, PCP, REH, SNO) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        set_TMN_result = f'INSERT INTO weather (fcstDate, fcstTime, TMP, UUU, VVV, VEC, WSD, SKY, PTY, POP, WAV, PCP, REH, SNO, TMN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        set_TMX_result = f'INSERT INTO weather (fcstDate, fcstTime, TMP, UUU, VVV, VEC, WSD, SKY, PTY, POP, WAV, PCP, REH, SNO, TMX) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        
        try:
            for i in range(len(ITEM)):
                # 정해진 순서대로 카테고리 값이 같다면
                if ITEM[i]['category'] == str(CODE_INFO[code_num]):
                    # 2차원 배열에 카테고리, 날짜, 시간 추가
                    # 만약 list_info[]에 데이터가 없다면
                    if code_num >= len(CODE_INFO):
                        code_num = 0
                    # data 리스트가 비어있다면 날짜 시간 값 추가
                    elif list_data == [] :
                        list_data.append(ITEM[i]['fcstDate'])
                        list_data.append(ITEM[i]['fcstTime'])
                        list_data.append(ITEM[i]['fcstValue'])
                        code_num += 1
                    # TMN가 수서대로 나왔을 경우
                    elif ITEM[i]['category'] == 'TMN':
                        list_data.append(ITEM[i]['fcstValue'])
                        list_data_detail.append(list_data)
                        cur.execute(set_TMN_result, (list_data))
                        list_data = []
                        code_num = 0
                    # 날짜랑 시간이 같다면 값 추가
                    elif ITEM[i]['fcstDate'] == list_data[0] and ITEM[i]['fcstTime'] == list_data[1]:
                        list_data.append(ITEM[i]['fcstValue'])
                        code_num += 1
                # 카테고리 값이 정해진 순서대로 안나왔을 경우
                elif ITEM[i]['category'] != str(CODE_INFO[code_num]):
                    # TMN을 뛰어넘고 TMX가 나왔을 경우
                    if ITEM[i]['category'] == 'TMX':
                        list_data.append(ITEM[i]['fcstValue'])
                        list_data_detail.append(list_data)
                        cur.execute(set_TMX_result, (list_data))
                        list_data = [] 
                        code_num = 0
                    # TMN, TMX가 나오지않고 건너 뛰었을 경우
                    elif ITEM[i]['category'] == 'TMP':
                        list_data_detail.append(list_data)
                        cur.execute(set_TMP_result, (list_data))
                        list_data = []
                        list_data.append(ITEM[i]['fcstDate'])
                        list_data.append(ITEM[i]['fcstTime'])
                        list_data.append(ITEM[i]['fcstValue'])
                        code_num = 1   
                    # 데이터 값 리스트에 저장
                    # 만약 list_info의 [i]번째 리스트 'fcstDate', 'fcstTime'가 같다면 append
                else:
                    i += 1
        except Exception as e:
            print(e)

        conn.commit()

        # 결과 가져오기
        print(cur.fetchall())
        conn.close()
        print('저장')

def main():
    weatherlogic = weather_Logic()
    weatherlogic.Short_term_checkDate()

if __name__ == '__main__':
    main()