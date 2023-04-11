import pymysql
import pandas as pd
from datetime import datetime as dt, timedelta as td
import datetime


# # 주현집 host
# conn = pymysql.connect(host='localhost', user = 'root', password='12345',
#                        db = 'miniproject', charset='utf8')
# cur = conn.cursor()
# query = '''SELECT DATE_FORMAT(fcstDate, '%Y%m%d'), date_format(fcstTime, '%H%i%s')
#                      FROM weather'''

# cur.execute(query) 
# rows = cur.fetchall()

# df = pd.DataFrame(rows)
# df.columns = ['date', 'time']
# print(df)
# ft = df[(df['date'] == '20230326') & (df['time'] == '090000')]
# print(len(ft))
# # print(df[df['date'] == '20230321' & df['time'] == '090000'])



for _ in range(1):
    print('*')
                       






