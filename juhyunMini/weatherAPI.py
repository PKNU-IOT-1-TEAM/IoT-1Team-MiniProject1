# API
from urllib.parse import urlencode # 한글을 URLencode 변환하는 함수
from datetime import datetime as dt, timedelta as td
import requests
import json
# MYSQL
import pymysql

def getDataPortalSearch(baseDate, baseTime):
    api_url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    queryString = '?' + urlencode(
        {
            'serviceKey': 'Hp7RL4tCw0cXBMTYsWCTrydbix/qtqe4+u5yRNze4LKbniVQhVKmNWMk8IxYObz6/EB41Vo47zCdEVUVRfAvsA==',
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'JSON',
            'base_date': baseDate,
            'base_time': baseTime,
            'nx': 98,
            'ny': 76
        }
    )
    total_url = api_url + queryString
    response = requests.get(total_url, verify=False)
    return response.text

def weatherData():   # respnse 데이터 가져와서 사용하기 좋게 가공
    
    # 검색 날짜, 시간 설정
    baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
    nowTime = int(dt.now().time().strftime("%H"))
    if nowTime == 24:
        baseTime = '2300'
    elif nowTime >= 21:
        baseTime = '2000'
    elif nowTime >= 18:
        baseTime = '1700'
    elif nowTime >= 15:
        baseTime = '1400'
    elif nowTime >= 12:
        baseTime = '1100'
    elif nowTime >= 9:
        baseTime = '0800'
    elif nowTime >= 6:
        baseTime = '0500'
    elif nowTime >= 3:
        baseTime = '0200'
    else:
        baseTime = '2300'
        baseDate = f'{(dt.now().date() - td(days=1)).strftime("%Y%m%d")}'
    
    try:
        result = getDataPortalSearch(baseDate, baseTime)
        json_data = json.loads(result)
        weather_data = json_data['response']['body']['items']['item']
    except Exception as e:
        print('찾는 데이터가 없습니다.')
    
    changeDate = weather_data[0]['fcstDate']
    changeTime = weather_data[0]['fcstTime']
    fcstData = dict()
    allFcstData = []

    for item in weather_data:
        del item['baseDate'], item['baseTime'], item['nx'], item['ny']
        if item['category'] == 'TMP':   # 온도
            item['tmp'] = item['fcstValue']
        elif item['category'] == 'VEC': # 풍향
            item['vec'] = item['fcstValue']
        elif item['category'] == 'WSD': # 풍속
            item['wsd'] = item['fcstValue']
        elif item['category'] == 'SKY': # 하늘 상태
            item['sky'] = item['fcstValue']
        elif item['category'] == 'PTY': # 강수 형태 
            item['wsd'] = item['fcstValue']
        elif item['category'] == 'POP': # 강수 확률
            item['pop'] = item['fcstValue']
        elif item['category'] == 'PCP': # 1시간 강수량
            item['pcp'] = item['fcstValue']
        elif item['category'] == 'REH': # 습도
            item['reh'] = item['fcstValue']
        elif item['category'] == 'SNO': # 신적설
            item['sno'] = item['fcstValue']
        elif item['category'] == 'TMN': # 하루 최저 온도
            item['tmn'] = item['fcstValue']
        elif item['category'] == 'TMM': # 하루 최고 온도
            item['tmm'] = item['fcstValue']
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

def insertDB():
    conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                           db = 'miniproject', charset='utf8')
    cur = conn.cursor()    # Connection으로부터 Cursor 생성

    allFcstData = weatherData()

    for fcstData in allFcstData:
        if 'tmn' in fcstData.keys():
            query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, POP, PCP, REH, SNO, TMN)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['tmp'],
                            fcstData['vec'], fcstData['wsd'], fcstData['sky'], fcstData['pop'],
                            fcstData['pcp'], fcstData['reh'], fcstData['sno'], fcstData['tmn']))
        elif 'tmm' in fcstData.keys():
            query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD, SKY, POP, PCP, REH, SNO, TMM)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['tmp'],
                            fcstData['vec'], fcstData['wsd'], fcstData['sky'], fcstData['pop'],
                            fcstData['pcp'], fcstData['reh'], fcstData['sno'], fcstData['tmm']))
        else:
            query = '''INSERT INTO weather (fcstDate, fcstTime, TMP, VEC, WSD,  SKY, POP, PCP, REH, SNO)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cur.execute(query, (fcstData['fcstDate'], fcstData['fcstTime'], fcstData['tmp'],
                            fcstData['vec'], fcstData['wsd'], fcstData['sky'], fcstData['pop'],
                            fcstData['pcp'], fcstData['reh'], fcstData['sno']))
            
        conn.commit()

    conn.close()
    print('저장')

insertDB()

