import requests
import json
import datetime

data = dict()
weather_data = dict()


url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
key = 'yR+IgD8xUGGLPLv5yhXB/1N8mrSZZShOsMcBdKjRIHdtT2R1/DttqVn95bmWMWkbyEbcz/J8qqJaoq5sRLTbbw=='

today = datetime.datetime.today()
base_date = today.strftime('%Y%m%d')
base_time = '0800'

nx = '35'
ny = '129'

payload = 'serviceKey=' + key + '&' +\
          'dataType=json' + '&' +\
          'base_date=' + base_date + '&' +\
          'base_time=' + base_time + '&' +\
          'nx=' + nx + '&' +\
          'ny=' + ny

res = requests.get(url + '?' + payload)
json_data = res.json()

response = json_data.get('response')
if response is not None:
    body = response.get('body')
    if body is not None:
        items = body.get('items')
        if items is not None:
            data['date'] = base_date
            for item in items['item']:
                if item['category'] == 'TMP':
                    weather_data['tmp'] = item['fcstValue']
                if item['category'] == 'PTY':
                    weather_code = item['fcstValue']

                    if weather_code == '1':
                        weather_state = '비'
                    elif weather_code == '2':
                        weather_state = '비/눈'
                    elif weather_state == '3':
                        weather_state = '눈'
                    elif weather_code == '4':
                        weather_state = '소나기'
                    else:
                        weather_state = '없음'

                    weather_data['code'] = weather_code
                    weather_data['state'] = weather_state

            data['weather'] = weather_data
else:
    print('Error: No "response" key in JSON data')