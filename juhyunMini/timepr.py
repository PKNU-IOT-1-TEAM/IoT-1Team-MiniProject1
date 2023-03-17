from datetime import datetime as dt, timedelta as td
import datetime

# 검색 날짜, 시간 설정
baseDate = f'{dt.now().date().strftime("%Y%m%d")}'
# nowTime = int(dt.now().time().strftime("%H"))
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

print(baseDate, baseTime)
