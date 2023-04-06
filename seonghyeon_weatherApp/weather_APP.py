import os
import sys
import pymysql
from datetime import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyqtgraph import *
import weather_API

today = datetime.today().strftime("%Y%m%d") # 특수문자 제거
tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
day_after_tomorrow = (date.today() + timedelta(days=2)).strftime("%Y%m%d")

now = datetime.now() # 오늘 시간
# 뽑아올 데이터 순서
select_data_list = ['fcstDate', 'fcstTime', 'POP', 'PTY', 'REH', 'SKY', 'TMP', 'WSD']
# 뽑아올 시간 순서
Date_list = [today, tomorrow, day_after_tomorrow]
# 일단 만들어놓고 생각하자 되긴 될거 같은데
labels = ['today_date', 'todayREH', 'todayPTY', 'todayTMP', 'todayVEC', 'todayWSD', 'todayPOP', 
           'tomorrow_date', 'tomorrowREH', 'tomorrowPTY', 'tomorrowTMP', 'tomorrowVEC', 'tomorrowWSD', 'tomorrowPOP',
           'day_after_tomorrow_date', 'day_after_tomorrowREH', 'day_after_tomorrowPTY', 'day_after_tomorrowTMP', 'day_after_tomorrowVEC', 'day_after_tomorrowWSD', 'day_after_tomorrowPOP']
# 리스트로 날씨를 받아올 거다.
weather_list = []

class MainWindow(QMainWindow):

    def __init__(self):    
        super().__init__()
        uic.loadUi('./seonghyeon_weatherApp/weatherApp.ui', self)
        # 라벨 값 교체
        self.today_date.setText(weather_list[0][0])
        self.todayREH.setText(weather_list[0][2])
        self.todayPTY.setText(weather_list[0][3])
        self.todayTMP.setText(weather_list[0][4])
        self.todayVEC.setText(weather_list[0][5])
        self.todayWSD.setText(weather_list[0][6])
        self.todayPOP.setText(weather_list[0][7])
        self.tomorrow_date.setText(weather_list[1][0])
        self.tomorrowREH.setText(weather_list[1][2])
        self.tomorrowPTY.setText(weather_list[1][3])
        self.tomorrowTMP.setText(weather_list[1][4])
        self.tomorrowVEC.setText(weather_list[1][5])
        self.tomorrowWSD.setText(weather_list[1][6])
        self.tomorrowPOP.setText(weather_list[1][7])
        self.day_after_tomorrow_date.setText(weather_list[2][0])
        self.day_after_tomorrowREH.setText(weather_list[2][2])
        self.day_after_tomorrowPTY.setText(weather_list[2][3])
        self.day_after_tomorrowTMP.setText(weather_list[2][4])
        self.day_after_tomorrowVEC.setText(weather_list[2][5])
        self.day_after_tomorrowWSD.setText(weather_list[2][6])
        self.day_after_tomorrowPOP.setText(weather_list[2][7])
        
    def initDB(self):
        global weather_list
        # (임시) 10시 전이면 12시 고정값으로 받아와서 일단 뿌리기
        if now.hour < 10:
            result_hour = '1200'
        else:
            result_hour = str(now.hour + 1) + '00'

        con = pymysql.connect(
            host = '127.0.0.1', 	 #ex) '127.0.0.1' "210.119.12.66"
            port = 3306,
            user = "root", 		 #ex) root
            password = "12345",
            database = "miniproject01", 
            charset = 'utf8'
        )
        cur = con.cursor()

        # 데이터 베이스에 접근해서 정해진 조건으로 검색해서 가져오기

        get_index_result = f'''SELECT fcstDate, fcstTime, REH, PTY, TMP, VEC, WSD, POP
                                 FROM parkseonghyeon
                                WHERE (fcstDate = {today} and fcstTime = {result_hour}) 
                                   or (fcstDate = {tomorrow} and fcstTime = {result_hour}) 
                                   or (fcstDate = {day_after_tomorrow} and fcstTime = {result_hour});'''
        cur.execute(get_index_result)
        # 불러온 값 전부 받아와서 유닛에 저장
        unit = cur.fetchall()
        # 리스트에 값 저장
        weather_list = unit
        print(unit)
        con.close()


def main():
    weather_API.main()
    MainWindow.initDB(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

