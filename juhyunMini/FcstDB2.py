# API
from urllib.parse import urlencode # 한글을 URLencode 변환하는 함수
from FcstAPI import *
import datetime
from datetime import datetime as dt, timedelta as td
import json
# MYSQL
import pymysql
# schedule
import schedule
import time
# pandas
import pandas as pd

# 개인
# conn = pymysql.connect(host='localhost', user = 'root', password='12345',
#                         db = 'miniproject', charset='utf8')
# 성현DB
# conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
#                     db = 'miniproject01', charset='utf8')


# 1. 처음 실행시 어제 오전 2시부터 현재 시각까지의 API 데이터 DB업데이트
# 2. API 기준시간에 자동으로 DB 업데이트
class FcstDB:
    def __init__(self) -> None:
        # 어제 API 데이터 DB삽입, 업데이트
        for pasttime in range(8):
            baseDate, baseTime = self.baseDateTime(-1, pasttime)    # 어제날짜, 시간
            if pasttime == 0:   # 첫 데이터는 DB Insert
                self.insertDB(baseDate, baseTime)
            else:   # DB Update
                self.updateDB(baseDate, baseTime)

        # 현재 시각까지 API 데이터 DB 업데이트
        num = self.baseDateTime(0)   # 반복 횟수 받기
        if num == -1:   # 현재시간이 오전 2시 이전이면 -1 -> API 업데이트할 거 없음
            pass
        else:
            for pasttime in range(num):
                baseDate, baseTime = self.baseDateTime(1, pasttime)
                self.updateDB(baseDate, baseTime)
        print('DB 초기화 완료')          

    def insertDB(self, baseDate, baseTime):        
        # DB connection
        conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                               db = 'miniproject', charset='utf8')
        cur = conn.cursor()    # Connection으로부터 Cursor 생성

        # DB 초기화
        query = '''TRUNCATE weather'''
        cur.execute(query)
        
        # API 데이터
        allFcstData = self.newData(baseDate, baseTime)
        # DB에 API 데이터 Insert
        for fcstData in allFcstData:
            self.insertQuery(fcstData, cur)                
            conn.commit()
        
        # DB connection 닫기
        conn.close()
        print(f'[{dt.now()}] [{baseDate} {baseTime}] DB 데이터 삽입')

    def insertQuery(self, fcstData, cur):
        if 'TMN' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, PTY, POP, PCP, REH, SNO, TMN)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'], fcstData['VEC'],
                                    fcstData['WSD'], fcstData['SKY'], fcstData['PTY'], fcstData['POP'],
                                    fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN']))
        elif 'TMM' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, PTY, POP, PCP, REH, SNO, TMM)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'], fcstData['VEC'],
                                        fcstData['WSD'], fcstData['SKY'], fcstData['PTY'], fcstData['POP'],
                                            fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMM']))
        else:
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, PTY, POP, PCP, REH, SNO)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'], fcstData['VEC'],
                                        fcstData['WSD'], fcstData['SKY'], fcstData['PTY'], fcstData['POP'],
                                        fcstData['PCP'], fcstData['REH'], fcstData['SNO']))

    def updateDB(self, baseDate, baseTime):
        # DB conn 연결
        conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                               db = 'miniproject', charset='utf8')        
        cur = conn.cursor()    # Connection으로부터 Cursor 생성
        # SELECT 쿼리문
        query = '''SELECT DATE_FORMAT(fcstDate, '%Y%m%d'), date_format(fcstTime, '%H%i%s')
                     FROM weather'''
        cur.execute(query) 
        rows = cur.fetchall()
        # DB데이터 pandas.DataFrame에 넣기
        df = pd.DataFrame(rows)
        df.columns = ['Date', 'Time']

        # API 데이터
        allFcstData = self.newData(baseDate, baseTime)
        # API, DB 데이터 비교하여 Update 또는 Insert
        for fcstData in allFcstData:
            # 날짜, 시간이 같은 데이터 행 조회
            exitdb = df[(df['Date'] == fcstData['fcstDate']) & (df['Time'] == fcstData['fcstTime'])]
            if len(exitdb): # 있다면 Update
                self.updateQuery(fcstData, cur)
            else:   # 없다면 Insert
                self.insertQuery(fcstData, cur)
            conn.commit()
        conn.close()
        print(f'[{dt.now()}] [{baseDate} {baseTime}] 기상DB 업데이트') 

    def updateQuery(self, fcstData, cur):
        if 'TMN' in fcstData.keys():
             query = '''UPDATE weather
                          SET TMP = %s, VEC = %s, WSD = %s, SKY = %s, PTY = %s, POP = %s, PCP = %s, REH = %s, SNO = %s, TMN = %s
                        WHERE fcstDate = %s + 00 And fcstTime = %s '''
             cur.execute(query, (fcstData['TMP'], fcstData['VEC'], fcstData['WSD']
                               , fcstData['SKY'], fcstData['PTY'], fcstData['POP']
                               , fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN'], fcstData['fcstDate'], fcstData['fcstTime']))
        elif 'TMM' in fcstData.keys():
             query = '''UPDATE weather
                          SET TMP = %s, VEC = %s, WSD = %s, SKY = %s, PTY = %s, POP = %s, PCP = %s, REH = %s, SNO = %s, TMM = %s
                        WHERE fcstDate = %s + 00 And fcstTime = %s '''
             cur.execute(query, (fcstData['TMP'], fcstData['VEC'], fcstData['WSD']
                               , fcstData['SKY'], fcstData['PTY'], fcstData['POP']
                               , fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMM'], fcstData['fcstDate'], fcstData['fcstTime']))
        else:
            query = '''UPDATE weather
                          SET TMP = %s, VEC = %s, WSD = %s, SKY = %s, PTY = %s, POP = %s, PCP = %s, REH = %s, SNO = %s
                        WHERE fcstDate = %s + 00 And fcstTime = %s '''
            cur.execute(query, (fcstData['TMP'], fcstData['VEC'], fcstData['WSD']
                               , fcstData['SKY'], fcstData['PTY'], fcstData['POP']
                               , fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['fcstDate'], fcstData['fcstTime']))
    
    def baseDateTime(self, mode, *pasttime):
        PARA_TIME = ['0200','0500', '0800', '1100', '1400', '1700', '2000', '2300']
        API_TIME = [datetime.time(2,10), datetime.time(5,10), datetime.time(8,10),
                            datetime.time(11,10), datetime.time(14,10), datetime.time(17,10),
                            datetime.time(20,10), datetime.time(23,10)]
        
        # 어제 오전 2시부터 오후 23시까지
        if mode == -1:           
            baseDate = f'{(dt.now().date() - td(days=1)).strftime("%Y%m%d")}'
            baseTime = PARA_TIME[pasttime[0]]      
        
        # 오늘중 현재시간까지의 API 기준시간 갯수
        elif mode == 0:   
            nowTime = dt.now().time()
            for i, time in enumerate(API_TIME[::-1]):
                if nowTime >= time:
                    # baseTime = PARA_TIME[i]
                    return (len(PARA_TIME)-i)
                elif nowTime < API_TIME[0]: # 현재 시각이 오전 2시이면 오늘 업데이트할 것 없음. 
                    return -1
                
        # 현재시간이전의 API 기준시간
        elif mode == 1:
            baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
            baseTime = PARA_TIME[pasttime[0]]
        
        # 자동 업데이트할 API 기준시간
        elif mode == 2:
            baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
            baseTime = f'{dt.now().time().strftime("%H")}00'

        return (baseDate, baseTime)
                       
    def newData(self, baseDate, baseTime):
        # 실제 API 데이터 가져오기
        api = FcstAPI() # API 객체 생성
        try:
            result = api.getDataPortalSearch(baseDate, baseTime)
            json_data = json.loads(result)
            newFcstData = json_data['response']['body']['items']['item']
        except Exception as e:
                print('찾는 데이터가 없습니다.')

        # 시각 별로 모으기 위해 날짜, 시간 변화에 대한 변수 선언
        changeDate = newFcstData[0]['fcstDate']
        changeTime = newFcstData[0]['fcstTime']
        
        fcstData = dict()
        allFcstData = []
        CATEGORY = ['TMP', 'VEC', 'WSD', 'SKY', 'PTY', 'POP', 'PCP', 'REH', 'SNO', 'TMN', 'TMM']

        for item in newFcstData:
            # 필요없는 것 삭제
            del item['baseDate'], item['baseTime'], item['nx'], item['ny']

            for category in CATEGORY:
                # item 딕셔너리 키,값 정리           
                if item['category'] == category:
                    # (key:카테고리 명/ value: 수치) 추가
                    item[f'{category}'] = item['fcstValue']
                    break
            # (key:카테고리, key: 수치) 데이터 삭제    
            del item['category'], item['fcstValue'] 

            # 날짜, 시간 같으면 정리한 item을 fcstDate에 쌓기
            if changeDate == item['fcstDate'] and changeTime == item['fcstTime']:
                fcstData = fcstData|item
            # 날짜,시간 다르면 같은 시각의 데이터들을 모은
            else:   # 딕셔너리fcstDate를 allFcstData에 추가하고 초기화하고 item 담기
                fcstData['fcstTime'] = fcstData['fcstTime'] + '00'  # TIME : 000000
                allFcstData.append(fcstData)
                fcstData = dict()
                fcstData = item
                changeDate = item['fcstDate']   # 날짜 변경
                changeTime = item['fcstTime']   # 시간 변경

        fcstData['fcstTime'] = fcstData['fcstTime'] + '00'        
        allFcstData.append(fcstData)    # 마지막 날짜시각 데이터 allFcstDate에 추가
        return allFcstData

    def autoUpdateDB(self): # 자동 DB 업데이트
        baseDate, baseTime = self.baseDateTime(2)
        self.updateDB(baseDate, baseTime)


if __name__ == '__main__':

    db = FcstDB()
    schedule.every().day.at("02:10").do(db.autoUpdateDB)
    schedule.every().day.at("05:10").do(db.autoUpdateDB)
    schedule.every().day.at("08:10").do(db.autoUpdateDB)
    schedule.every().day.at("11:10").do(db.autoUpdateDB)
    schedule.every().day.at("14:10").do(db.autoUpdateDB)
    schedule.every().day.at("17:10").do(db.autoUpdateDB)
    schedule.every().day.at("20:10").do(db.autoUpdateDB)
    schedule.every().day.at("23:10").do(db.autoUpdateDB)

    while True:
        schedule.run_pending()