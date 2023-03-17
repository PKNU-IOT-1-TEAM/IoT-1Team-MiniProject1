# API
from urllib.parse import urlencode # 한글을 URLencode 변환하는 함수
from FcstAPI import *
import datetime
from datetime import datetime as dt, timedelta as td
import requests
import json
# MYSQL
import pymysql

class FcstDB:
    def __init__(self) -> None:
        print(f'[{dt.now()}] 기상DB 생성')
        self.insertDB()

    def insertDB(self):
        # 주현집 host
        # conn = pymysql.connect(host='localhost', user = 'root', password='12345',
        #                        db = 'miniproject', charset='utf8')
        # 성현DB
        conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
                            db = 'miniproject01', charset='utf8')
        cur = conn.cursor()    # Connection으로부터 Cursor 생성

        allFcstData = self.newData()

        for fcstData in allFcstData:
            if 'TMN' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, POP, PCP, REH, SNO, TMN)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
                                fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
                                fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN']))
            elif 'TMM' in fcstData.keys():
                query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, , WSD, SKY, POP, PCP, REH, SNO, TMM)
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
        print('DB저장완료')
    
    def updateDB(self):
        pass
        # 성현DB
        # conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
        #                     db = 'miniproject01', charset='utf8')
        # cur = conn.cursor()    # Connection으로부터 Cursor 생성

        # allFcstData = self.newData()

        # for fcstData in allFcstData:
        #     if 'TMN' in fcstData.keys():
        #         query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, POP, PCP, REH, SNO, TMN)
        #                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        #         cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
        #                         fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
        #                         fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMN']))
        #     elif 'TMM' in fcstData.keys():
        #         query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, , WSD, SKY, POP, PCP, REH, SNO, TMM)
        #                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        #         cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
        #                         fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
        #                         fcstData['PCP'], fcstData['REH'], fcstData['SNO'], fcstData['TMM']))
        #     else:
        #         query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD,  SKY, POP, PCP, REH, SNO)
        #                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        #         cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['TMP'],
        #                         fcstData['VEC'], fcstData['WSD'], fcstData['SKY'], fcstData['POP'],
        #                         fcstData['PCP'], fcstData['REH'], fcstData['SNO']))
                
        #     conn.commit()

        # conn.close()
        # print('DB저장완료')


    def newData(self):
        # 검색 날짜 설정
        baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
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
    

re = FcstDB()