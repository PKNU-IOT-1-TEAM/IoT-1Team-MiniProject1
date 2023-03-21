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

# 개인DB
# conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                        # db = 'miniproject', charset='utf8')
# 성현DB
# conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
#                     db = 'miniproject01', charset='utf8')


# 1. 처음 실행시 현재 시각기준으로 DB삽입
# 2. API 기준 시간되면 자동으로 DB 업데이트
# 3. TEST를 위한 임의 시각도 가능
class FcstDB:
    # 처음 실행시 현재 시각기준으로 DB 삽입
    def __init__(self) -> None:
        self.insertDB(1)
        print(f'[{dt.now()}] 기상DB 생성 완료')

    def updateDB(self, mode, *setDate):
        if mode == 0:   # Mode: 0 설정한 시간에 API
            allFcstData = self.newData(mode) 
        if mode == 2:   # Mode: 2 업데이트동작 TEST를 위해 임의로 설정한 시간기준 API
             allFcstData = self.newData(mode, setDate[0], setDate[1])

        # DB Connection
        conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                               db = 'miniproject', charset='utf8')
        cur = conn.cursor()    # Connection으로부터 Cursor 생성
        # SELECT 쿼리문
        query = '''SELECT Idx, fcstDate, fcstTime
                     FROM weather'''
        cur.execute(query) 
        exits = cur.fetchall()
        # print(currentDB)
        
        # API, DB 데이터 비교하여 업데이트 또는 삽입
        for fcstData in allFcstData:
            change = False
            for exit in exits:      # DB에 이미 존재하는 데이터일 경우 업데이트       
                if fcstData['fcstDate'] == str(exit['fcstDate']).replace('-', '') and \
                   str(fcstData['fcstTime'])+'00' == ((lambda x: '0' + x if len(x) < 8 else x)(str(exit['fcstTime']))).replace(':', ''):
                        self.updateQuery(fcstData, cur)
                        change = True
                        break
            if change == False:     # DB에 이미 존재하지 않을 경우 데이터일 경우 삽입
                 self.insertQuery(fcstData, cur)
            conn.commit()
        conn.close()    

    # 업데이트 쿼리문
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

    # 삽입 쿼리문        
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
        # DB Connection
        conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                               db = 'miniproject', charset='utf8')
        cur = conn.cursor()    # Connection으로부터 Cursor 생성

        # TRUNCATE 쿼리문
        query = '''TRUNCATE weather'''
        cur.execute(query)

        # API 불러와서 INSERT쿼리문 실행
        allFcstData = self.newData(mode)
        for fcstData in allFcstData:
            self.insertQuery(fcstData, cur)                
            conn.commit()
        conn.close()
        print('DB 데이터 삽입')
    
    # API
    def newData(self, mode, *setDate):
        # 검색 날짜 설정
        baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
        if mode == 1:    # mode:1 첫 실행시 현재 시각 기준으로 데이터 삽입
            nowTime = dt.now().time()
            API_TIME = [datetime.time(2,10), datetime.time(5,10), datetime.time(8,10),
                        datetime.time(11,10), datetime.time(14,10), datetime.time(17,10),
                        datetime.time(20,10), datetime.time(23,10)]
            # 현재시각을 API 검색 시각으로 변환
            for i, time in enumerate(API_TIME[::-1]):
                if nowTime >= time:
                    baseTime = f'{time.strftime("%H")}00'
                    break
                elif nowTime < API_TIME[0]: # 00시 ~ 2시10분 사이는 검색시간을 전날 23시로 설정 
                    baseDate = f'{(dt.now().date() - td(days=1)).strftime("%Y%m%d")}'
                    baseTime = f'{API_TIME[i-1].strftime("%H")}00'
                    break
        elif mode == 2: # mode:2 TEST
             baseDate = setDate[0]
             baseTime = setDate[1]

        else:   # mode: 0 정해진 시간에 자동 업데이트  
            baseTime = f'{dt.now().time().strftime("%H")}00'

        # 실제 API 데이터 가져오기
        api = FcstAPI() # API 객체 생성
        try:
            result = api.getDataPortalSearch(baseDate, baseTime)
            json_data = json.loads(result)
            newFcstData = json_data['response']['body']['items']['item']
        except Exception as e:
                print('찾는 데이터가 없습니다.')

        # 날짜,시간 별로 모으기 위해 날짜, 시간 변화에 대한 변수 선언
        changeDate = newFcstData[0]['fcstDate']
        changeTime = newFcstData[0]['fcstTime']
        fcstData = dict()   # FOR문 돌면서 날짜,시간별 모든 요소 데이터 담기위한 사전
        allFcstData = []    # 전체 데이터 리스트
        CATEGORY = ['TMP', 'VEC', 'WSD', 'SKY', 'PTY', 'POP', 'PCP', 'REH', 'SNO', 'TMN', 'TMM']
        # print(newFcstData)
        for item in newFcstData:
            print(item['fcstDate'], item['fcstTime'])
            del item['baseDate'], item['baseTime'], item['nx'], item['ny']  # 필요없는 것 삭제

            for category in CATEGORY:
            # item 딕셔너리 키,값 정리           
                if item['category'] == category:
                    item[f'{category}'] = item['fcstValue'] # (key:카테고리 명/ value: 수치) 데이터 추가
                    break
                
            del item['category'], item['fcstValue'] # (key:카테고리, key: 수치) 데이터 삭제

            if changeDate == item['fcstDate'] and changeTime == item['fcstTime']:
                fcstData = fcstData|item    # 날짜, 시간 같으면 정리한 item을 fcstDate에 쌓기
            else:   # 날짜,시간 다르면 
                allFcstData.append(fcstData)    # allFcstData(전체 데이터)에 같은 시각의 데이터를 모은 fcstDate 추가
                fcstData = dict()   # 다음 시각의 데이터를 모으기 위해 초기화후 item 대입
                fcstData = item 
                changeDate = item['fcstDate']   # 날짜 바꾸기
                changeTime = item['fcstTime']   # 시간 바꾸기

        allFcstData.append(fcstData)    # 마지막 날짜시각 데이터도 allFcstDate에 추가
        # print(allFcstData)
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
