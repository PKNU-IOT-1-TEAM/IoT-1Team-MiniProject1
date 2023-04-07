import requests # 기본적인 URL 모듈로는 안되서 대체
import json
import pymysql 
import urllib3
import os

from mysql.connector import *

from datetime import *

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pyqtgraph import *

from urllib.request import *
from urllib.parse import *  # 한글을 URLencode 변환하는 함수

# API에서 제공하는 데이터 순서
CODE_INFO = ['TMP','UUU','VVV','VEC','WSD','SKY','PTY','POP','WAV','PCP','REH','SNO','TMN', 'TMX'  ]
# API 데이터가 갱신되는 기준 시간
API_TIME = [2, 5, 8, 11, 14, 17, 20, 23]
# API 데이터는 10분에 업데이트 해준다.
API_MINUTE = 10
# 오류 안띄우기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


today = datetime.today().strftime("%Y%m%d") # 특수문자 제거
tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
day_after_tomorrow = (date.today() + timedelta(days=2)).strftime("%Y%m%d")

now = datetime.now() # 오늘 시간
# 뽑아올 데이터 순서
select_data_list = ['fcstDate', 'fcstTime', 'POP', 'PTY', 'REH', 'SKY', 'TMP', 'WSD']
# 뽑아올 시간 순서
Date_list = [today, tomorrow, day_after_tomorrow]
# 일단 만들어놓고 생각하자 되긴 될거 같은데
# labels = ['today_date', 'todayREH', 'todayPTY', 'todayTMP', 'todayVEC', 'todayWSD', 'todayPOP', 
#            'tomorrow_date', 'tomorrowREH', 'tomorrowPTY', 'tomorrowTMP', 'tomorrowVEC', 'tomorrowWSD', 'tomorrowPOP',
#            'day_after_tomorrow_date', 'day_after_tomorrowREH', 'day_after_tomorrowPTY', 'day_after_tomorrowTMP', 'day_after_tomorrowVEC', 'day_after_tomorrowWSD', 'day_after_tomorrowPOP']
# 리스트로 날씨를 받아올 거다.
weather_list = []

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
        # API 제공 시간 횟수만큼 반복
        for time in range(len(API_TIME)):
            now_time = str(API_TIME[time]) + str(API_MINUTE) # 현재와 제일 가까운 시간
            pre_time = str(API_TIME[time - 1]) + str(API_MINUTE) # 이전 시간 - 발표 시간 시간 사이에 끼어있는 애매한 시간
            y_time = str(API_TIME[7]) + str(API_MINUTE) # 전날 마지막 시간
            # 지금 시간이 시간 API_TIME 원소랑 같고 10분보다 크거나 같을 경우
            if now.hour is API_TIME[time] and now.minute >= API_MINUTE:
                # 10시보다 작을 경우
                if now.hour < 10:
                    # 업데이트 기준 날짜는 오늘
                    base_date = today
                    # 시간이 3자리라서 0이 앞에 붙어줘야한다.
                    base_time = '0' + now_time
                    # 날짜 시간 지정해주고 반복문 탈출
                    break
                else: # 10시보다 큰 경우
                    # 업데이트 기준 날짜는 오늘
                    base_date = today
                    # 시간은 지금 시간
                    base_time = now_time
                    # 날짜 시간 지정해주고 반복문 탈출
                    break
            # 시간과 시간 사이에 끼어있는 애매한 시간일 경우
            elif API_TIME[time - 1] < now.hour <= API_TIME[time]:
                # 시간이 10시보다 작을 경우
                if now.hour < 10:
                    # 업데이트 기준 날짜는 오늘
                    base_date = today
                    # 시간이 3자리라서 0이 앞에 붙어줘야한다.
                    base_time = '0' + pre_time
                    # 날짜 시간 지정해주고 반복문 탈출
                    break 
                # 시간이 10시 보다 클 경우
                else:
                    # 업데이트 기준 날짜는 오늘
                    base_date = today
                    # 시간은 지금 시간
                    base_time = pre_time
                    # 날짜 시간 지정해주고 반복문 탈출
                    break
            # 시간이 2시보다 작을 경우
            elif now.hour < API_TIME[0]:
                # 업데이트 기준 날짜는 어제(아직 오늘껀 발표 안났으니까)
                base_date = yesterday
                # 시간은 어제 기준
                base_time = y_time
                # 날짜 시간 지정해주고 반복문 탈출
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
        # json을 읽어와서 텍스트 형식으로 json_data에 대입
        json_data = json.loads(response.text)
        # 딕셔너리로 json을 옮겨왔기 때문에 
        # response value 값인 
        # body 안에 있는 value 값인
        # items 안에 있는 value 값인
        # item 안에 있는 value 값에 접근
        ITEM = json_data['response']['body']['items']['item']
        
        list_data = []  # 1차원 배열
        list_data_detail = []  # 2차원 배열
        # 2차원 배열로 단기예보 항목명, 날짜, 시간 별로 구분
        code_num = 0

        # DB 연결
        conn = pymysql.connect(
            host = '127.0.0.1', 	 # ex) '127.0.0.1' "210.119.12.66"
            port = 3306,
            user = "root", 		 # ex) root
            password = "12345",
            database = "miniproject01", 
            charset = 'utf8'
        )
        # Cursor Object 가져오기
        cur = conn.cursor()
        # 쿼리 초기화(임시)
        query = '''DELETE FROM parkseonghyeon``'''
        # 쿼리문 날리기
        cur.execute(query)
        # 테이블 선택(임시)
        get_index_result = f'SELECT * FROM parkseonghyeon;'
        # 쿼리문 날리기
        cur.execute(get_index_result)
        # TMP, TMN, TMX 별로 쿼리문 따로 짜기
        set_TMP_result = f'INSERT INTO parkseonghyeon (fcstDate, fcstTime, TMP, UUU, VVV, VEC, WSD, SKY, PTY, POP, WAV, PCP, REH, SNO) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        set_TMN_result = f'INSERT INTO parkseonghyeon (fcstDate, fcstTime, TMP, UUU, VVV, VEC, WSD, SKY, PTY, POP, WAV, PCP, REH, SNO, TMN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        set_TMX_result = f'INSERT INTO parkseonghyeon (fcstDate, fcstTime, TMP, UUU, VVV, VEC, WSD, SKY, PTY, POP, WAV, PCP, REH, SNO, TMX) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        
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
                    # TMN가 순서대로 나왔을 경우
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

class MainWindow(QMainWindow):

    def __init__(self):    
        super().__init__()
        uic.loadUi('./seonghyeon_weatherApp/weatherApp.ui', self)
        # 라벨 값 교체
        self.today_date.setText(weather_list[0][0])
        self.todayREH.setText(weather_list[0][2])
        self.todayPTY.setText(weather_list[0][3])
        self.todayTMP.setText(weather_list[0][4])
        self.todayVEC.setText(weather_list[0][5])
        self.todayWSD.setText(weather_list[0][6])
        self.todayPOP.setText(weather_list[0][7])
        self.tomorrow_date.setText(weather_list[1][0])
        self.tomorrowREH.setText(weather_list[1][2])
        self.tomorrowPTY.setText(weather_list[1][3])
        self.tomorrowTMP.setText(weather_list[1][4])
        self.tomorrowVEC.setText(weather_list[1][5])
        self.tomorrowWSD.setText(weather_list[1][6])
        self.tomorrowPOP.setText(weather_list[1][7])
        self.day_after_tomorrow_date.setText(weather_list[2][0])
        self.day_after_tomorrowREH.setText(weather_list[2][2])
        self.day_after_tomorrowPTY.setText(weather_list[2][3])
        self.day_after_tomorrowTMP.setText(weather_list[2][4])
        self.day_after_tomorrowVEC.setText(weather_list[2][5])
        self.day_after_tomorrowWSD.setText(weather_list[2][6])
        self.day_after_tomorrowPOP.setText(weather_list[2][7])
        
    def initDB(self):
        global weather_list
        # (임시) 10시 전이면 12시 고정값으로 받아와서 일단 뿌리기
        if now.hour < 10:
            result_hour = '1200'
        else:
            result_hour = str(now.hour + 1) + '00'

        con = pymysql.connect(
            host = '127.0.0.1', 	 #ex) '127.0.0.1' "210.119.12.66"
            port = 3306,
            user = "root", 		 #ex) root
            password = "12345",
            database = "miniproject01", 
            charset = 'utf8'
        )
        cur = con.cursor()

        # 데이터 베이스에 접근해서 정해진 조건으로 검색해서 가져오기

        get_index_result = f'''SELECT fcstDate, fcstTime, REH, PTY, TMP, VEC, WSD, POP
                                 FROM parkseonghyeon
                                WHERE (fcstDate = {today} and fcstTime = {result_hour}) 
                                   or (fcstDate = {tomorrow} and fcstTime = {result_hour}) 
                                   or (fcstDate = {day_after_tomorrow} and fcstTime = {result_hour});'''
        cur.execute(get_index_result)
        # 불러온 값 전부 받아와서               // 유닛에 저장
        # 리스트에 값 저장
        weather_list = cur.fetchall()
        # weather_list = unit
        print(weather_list)
        con.close()

