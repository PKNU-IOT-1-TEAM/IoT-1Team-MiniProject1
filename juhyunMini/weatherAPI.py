# API
from urllib.parse import urlencode # 한글을 URLencode 변환하는 함수
from datetime import datetime as dt
import requests
import json
# MYSQL
import pymysql

def getDataPortalSearch(date, time):
    api_url = 'https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    queryString = '?' + urlencode(
        {
            'serviceKey': 'Hp7RL4tCw0cXBMTYsWCTrydbix/qtqe4+u5yRNze4LKbniVQhVKmNWMk8IxYObz6/EB41Vo47zCdEVUVRfAvsA==',
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'JSON',
            'base_date': date,
            'base_time': time,
            'nx': 98,
            'ny': 76
        }
    )
    total_url = api_url + queryString
    response = requests.get(total_url, verify=False)
    return response.text

def weaterData():   # respnse 데이터 
    
    date = f'{dt.now().date().strftime("%Y%m%d")}'
    # time = f'{dt.now().time().strftime("%H%M")}'
    time = '0500'
    
    try:
        result = getDataPortalSearch(date, time)
        # print(result)
        json_data = json.loads(result)
        weather_data = json_data['response']['body']['items']['item']
        # print(weather_data)
        # for item in weather_data:
            # print(item) # 딕셔너리
    except Exception as e:
        print('찾는 데이터가 없습니다.')

    conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
                            db = 'miniproject01', charset='utf8')
    cur = conn.cursor()    # Connection으로부터 Cursor 생성
    
    
    for item in weather_data:
        # if item['fcstDate'] == date:
        #     day1 = {fcstDate: }
        if item['category'] == 'TMP':
            fcstDate = item['fcstDate']
            fcstTime = item['fcstTime']
            tmp = item['fcstValue']
            # print(fcstDate, fcstTime, tmp)
            query = '''INSERT INTO juhyunlee (fcstDate, fcstTime, TMP)
                            VALUES (%s, %s, %s)'''
            cur.execute(query, (fcstDate, fcstTime, tmp))
            conn.commit()
    
    conn.close()
    print('저장')


weaterData()


