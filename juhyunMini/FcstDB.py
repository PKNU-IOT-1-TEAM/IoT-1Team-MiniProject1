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

# 처음 db 삽입 후 설정한 시간되면 자동으로 업데이트
class FcstDB:
    def __init__(self) -> None:
        self.insertDB(1)
        print(f'[{dt.now()}] 기상DB 생성 완료')

    def updateDB(self, mode, *setDate):
        if mode == 0:
            allFcstData = self.newData(0)    # API  0: 자동 시간
        if mode == 2:
             allFcstData = self.newData(2, setDate[0], setDate[1])
        # DB
        conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
                            db = 'miniproject01', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()    # Connection으로부터 Cursor 생성
        query = '''SELECT Idx, fcstDate, fcstTime
                     FROM weather'''
        cur.execute(query) 
        exits = cur.fetchall()
        # print(currentDB)
        
        # API, DB 데이터 비교하여 업데이트 OR 삽입
        for fcstData in allFcstData:
            change = False
            for exit in exits:                
                if fcstData['fcstDate'] == str(exit['fcstDate']).replace('-', '') and \
                   str(fcstData['fcstTime'])+'00' == ((lambda x: '0' + x if len(x) < 8 else x)(str(exit['fcstTime']))).replace(':', ''):
                        self.updateQuery(fcstData, cur)
                        change = True
                        break
            if change == False:
                 self.insertQuery(fcstData, cur)
            conn.commit()
        conn.close()    

    def updateQuery(self, fcstData, cur):
        if 'TMN' in fcstData.keys():
             query = '''UPDATE weather
                          SET TMP = %s, VEC = %s, WSD = %s, SKY = %s, PTY = %s, POP = %s, PCP = %s, REH = %s, SNO = %s, TMN = %s
                        WHERE fcstDate = %s + 00 And fcstTime = %s + 00 '''
             cur.execute(query, (fcstData['TMP'], fcstData['VEC'], fcstData['WSD']
                               , fcstData['SKY'], fcstData['PTY'], fcstData['POP']
                               , fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN'], fcstData['fcstDate'], fcstData['fcstTime']))
        elif 'TMM' in fcstData.keys():
             query = '''UPDATE weather
                          SET TMP = %s, VEC = %s, WSD = %s, SKY = %s, PTY = %s, POP = %s, PCP = %s, REH = %s, SNO = %s, TMM = %s
                        WHERE fcstDate = %s + 00 And fcstTime = %s + 00 '''
             cur.execute(query, (fcstData['TMP'], fcstData['VEC'], fcstData['WSD']
                               , fcstData['SKY'], fcstData['PTY'], fcstData['POP']
                               , fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMM'], fcstData['fcstDate'], fcstData['fcstTime']))
        else:
            query = '''UPDATE weather
                          SET TMP = %s, VEC = %s, WSD = %s, SKY = %s, PTY = %s, POP = %s, PCP = %s, REH = %s, SNO = %s
                        WHERE fcstDate = %s + 00 And fcstTime = %s + 00 '''
            cur.execute(query, (fcstData['TMP'], fcstData['VEC'], fcstData['WSD']
                               , fcstData['SKY'], fcstData['PTY'], fcstData['POP']
                               , fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['fcstDate'], fcstData['fcstTime']))
              
    def insertQuery(self, fcstData, cur):
        if 'TMN' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, PTY, POP, PCP, REH, SNO, TMN)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime']+'00', fcstData['TMP'], fcstData['VEC'],
                                    fcstData['WSD'], fcstData['SKY'], fcstData['PTY'], fcstData['POP'],
                                    fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN']))
        elif 'TMM' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, PTY, POP, PCP, REH, SNO, TMM)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime']+'00', fcstData['TMP'], fcstData['VEC'],
                                        fcstData['WSD'], fcstData['SKY'], fcstData['PTY'], fcstData['POP'],
                                            fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMM']))
        else:
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, PTY, POP, PCP, REH, SNO)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime']+'00', fcstData['TMP'], fcstData['VEC'],
                                        fcstData['WSD'], fcstData['SKY'], fcstData['PTY'], fcstData['POP'],
                                        fcstData['PCP'], fcstData['REH'], fcstData['SNO']))

    def insertDB(self, mode):
        # 주현집 host
        # conn = pymysql.connect(host='localhost', user = 'root', password='12345',
        #                        db = 'miniproject', charset='utf8')
        # 성현DB
        conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
                            db = 'miniproject01', charset='utf8')
        cur = conn.cursor()    # Connection으로부터 Cursor 생성

        query = '''TRUNCATE weather'''
        cur.execute(query)

        allFcstData = self.newData(mode)   # API 날짜 mode = 1 현재시간
        for fcstData in allFcstData:
            self.insertQuery(fcstData, cur)                
            conn.commit()
        conn.close()
        print('DB 데이터 삽입')
    
    def newData(self, mode, *setDate):
        # 검색 날짜 설정
        baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
        if mode == 1:    # 초기화 첫 시간으로 데이터 삽입
            nowTime = dt.now().time()
            API_TIME = [datetime.time(2,10), datetime.time(5,10), datetime.time(8,10),
                        datetime.time(11,10), datetime.time(14,10), datetime.time(17,10),
                        datetime.time(20,10), datetime.time(23,10)]

            for i, time in enumerate(API_TIME[::-1]):
                if nowTime >= time:
                    baseTime = f'{time.strftime("%H")}00'
                    break
                elif nowTime < API_TIME[0]:
                    baseDate = f'{(dt.now().date() - td(days=1)).strftime("%Y%m%d")}'
                    baseTime = f'{API_TIME[i-1].strftime("%H")}00'
                    break
        elif mode == 2:
             baseDate = setDate[0]
             baseTime = setDate[1]

        else:   # 정해진 시간에 자동 업데이트  
            baseTime = f'{dt.now().time().strftime("%H")}00'

        # 실제 데이터 가져오기
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
                allFcstData.append(fcstData)
                fcstData = dict()
                fcstData = item
        
            changeDate = item['fcstDate']
            changeTime = item['fcstTime']

        return allFcstData
    
if __name__ == '__main__':

    db = FcstDB()
    # db.updateDB(2, '20230320', '0200')    # mode 2 실행 되는지  test용
    # 매일 설정된 시간에 자동으로 데이터 삽입
    schedule.every().day.at("02:10").do(db.updateDB, 0)
    schedule.every().day.at("05:10").do(db.updateDB, 0)
    schedule.every().day.at("08:10").do(db.updateDB, 0)
    schedule.every().day.at("11:10").do(db.updateDB, 0)
    schedule.every().day.at("14:10").do(db.updateDB, 0)
    schedule.every().day.at("17:10").do(db.updateDB, 0)
    schedule.every().day.at("20:10").do(db.updateDB, 0)
    schedule.every().day.at("23:10").do(db.updateDB, 0)

    while True:
        schedule.run_pending()
