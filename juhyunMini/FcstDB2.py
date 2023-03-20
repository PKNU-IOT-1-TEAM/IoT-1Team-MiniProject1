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

# 주현 host
# conn = pymysql.connect(host='localhost', user = 'root', password='12345',
#                         db = 'miniproject', charset='utf8')
# 성현DB
# conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
#                     db = 'miniproject01', charset='utf8')


# API, DB 데이터 삽입, 업데이트
class FcstDB:

    def __init__(self) -> None:
        self.mode, self.i = -1, 0
        # 어제 데이터
        baseDate, baseTime = self.baseDateTime()
        self.insertDB(baseDate, baseTime)

        for _ in range(7):
            baseDate, baseTime = self.baseDateTime()
            self.updateDB(baseDate, baseTime)

        # 현재 시각까지 데이터
        self.mode, self.i = 0, 0
        num = self.baseDateTime()
        if num == -1:
            pass
        else:
            self.mode = 1
            for _ in range(num):
                baseDate, baseTime = self.baseDateTime()
                self.updateDB(baseDate, baseTime)
        print('DB 초기화 완료')
        mode = 2             

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
        # DB에 API 데이터 삽입
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
        # API, DB 데이터 비교하여 업데이트 OR 삽입
        for fcstData in allFcstData:
            exitdb = df[(df['Date'] == fcstData['fcstDate']) & (df['Time'] == fcstData['fcstTime'])]
            if len(exitdb):
                self.updateQuery(fcstData, cur)
            else:
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
    
    def baseDateTime(self):
        PARA_TIME = ['0200','0500', '0800', '1100', '1400', '1700', '2000', '2300']
        API_TIME = [datetime.time(2,10), datetime.time(5,10), datetime.time(8,10),
                            datetime.time(11,10), datetime.time(14,10), datetime.time(17,10),
                            datetime.time(20,10), datetime.time(23,10)]
        
        # 어제 오전 2시부터 오후 23시까지 8번 업데이트
        if self.mode == -1:           
            baseDate = f'{(dt.now().date() - td(days=1)).strftime("%Y%m%d")}'
            baseTime = PARA_TIME[self.i]
            # print(PARA_TIME[self.i])
            self.i += 1    
            return (baseDate, baseTime)

        elif self.mode == 0:
            nowTime = dt.now().time()
            for i, time in enumerate(API_TIME[::-1]):
                if nowTime >= time:
                    # baseTime = PARA_TIME[i]
                    return (len(PARA_TIME)-i)
                elif nowTime < API_TIME[0]:
                    return -1
                
        elif self.mode == 1:
            baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
            baseTime = PARA_TIME[self.i]
            # print(PARA_TIME[self.i])
            self.i += 1    
            return (baseDate, baseTime)
        
        elif self.mode == 2:
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

        changeDate = newFcstData[0]['fcstDate']
        changeTime = newFcstData[0]['fcstTime']
        
        fcstData = dict()
        allFcstData = []
        CATEGORY = ['TMP', 'VEC', 'WSD', 'SKY', 'PTY', 'POP', 'PCP', 'REH', 'SNO', 'TMN', 'TMM']

        for item in newFcstData:
            del item['baseDate'], item['baseTime'], item['nx'], item['ny']

            for category in CATEGORY:           
                if item['category'] == category:
                    item[f'{category}'] = item['fcstValue']
                    break
                
            del item['category'], item['fcstValue']

            if changeDate == item['fcstDate'] and changeTime == item['fcstTime']:
                fcstData = fcstData|item
            else:
                fcstData['fcstTime'] = fcstData['fcstTime'] + '00'  # TIME : 000000
                allFcstData.append(fcstData)
                fcstData = dict()
                fcstData = item
                changeDate = item['fcstDate']
                changeTime = item['fcstTime']

        fcstData['fcstTime'] = fcstData['fcstTime'] + '00'        
        allFcstData.append(fcstData)
        return allFcstData

    def autoUpdateDB(self):
        baseDate, baseTime = self.baseDateTime()
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