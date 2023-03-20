import os
import sys
import pymysql
from datetime import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyqtgraph import *

today = datetime.today().strftime("%Y%m%d") # 특수문자 제거
tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
day_after_tomorrow = (date.today() + timedelta(days=2)).strftime("%Y%m%d")

select_data_list = ['fcstDate', 'fcstTime', 'POP', 'PTY', 'REH', 'SKY', 'TMP', 'WSD']
Date_list = [today, tomorrow, day_after_tomorrow]

labels = ['today_date', 'todayREH', 'todayPTY', 'todayTMP', 'todayVEC', 'todayWSD', 'todayPOP', 
           'tomorrow_date', 'tomorrowREH', 'tomorrowPTY', 'tomorrowTMP', 'tomorrowVEC', 'tomorrowWSD', 'tomorrowPOP',
           'day_after_tomorrow_date', 'day_after_tomorrowREH', 'day_after_tomorrowPTY', 'day_after_tomorrowTMP', 'day_after_tomorrowVEC', 'day_after_tomorrowWSD', 'day_after_tomorrowPOP']

weather_list = []

class MainWindow(QMainWindow):

    def __init__(self):    
        super().__init__()
        uic.loadUi('./seonghyeon_weatherApp/weatherApp.ui', self)
        
        self.today_date.setText(weather_list[0][0])
        self.todayREH.setText(weather_list[0][1])
        self.todayPTY.setText(weather_list[0][2])
        self.todayTMP.setText(weather_list[0][3])
        self.todayVEC.setText(weather_list[0][4])
        self.todayWSD.setText(weather_list[0][5])
        self.todayPOP.setText(weather_list[0][6])
        self.tomorrow_date.setText(weather_list[1][0])
        self.tomorrowREH.setText(weather_list[1][1])
        self.tomorrowPTY.setText(weather_list[1][2])
        self.tomorrowTMP.setText(weather_list[1][3])
        self.tomorrowVEC.setText(weather_list[1][4])
        self.tomorrowWSD.setText(weather_list[1][5])
        self.tomorrowPOP.setText(weather_list[1][6])
        self.day_after_tomorrow_date.setText(weather_list[2][0])
        self.day_after_tomorrowREH.setText(weather_list[2][1])
        self.day_after_tomorrowPTY.setText(weather_list[2][2])
        self.day_after_tomorrowTMP.setText(weather_list[2][3])
        self.day_after_tomorrowVEC.setText(weather_list[2][4])
        self.day_after_tomorrowWSD.setText(weather_list[2][5])
        self.day_after_tomorrowPOP.setText(weather_list[2][6])
        
    def initDB(self):
        global weather_list
        con = pymysql.connect(
            host = '210.119.12.66', 	 #ex) '127.0.0.1' "210.119.12.66"
            port = 3306,
            user = "root", 		 #ex) root
            password = "12345",
            database = "miniproject01", 
            charset = 'utf8'
        )
        cur = con.cursor()

        # 데이터 베이스에 접근해서 정해진 조건으로 검색해서 가져오기

        get_index_result = f'''SELECT fcstDate, fcstTime, POP, PTY, REH, SKY, TMP, WSD
                                 FROM parkseonghyeon
                                WHERE (fcstDate = {today} and fcstTime = 1200) 
                                   or (fcstDate = {tomorrow} and fcstTime = 1200) 
                                   or (fcstDate = {day_after_tomorrow} and fcstTime = 1200);'''
        cur.execute(get_index_result)
        unit = cur.fetchall()
        weather_list = unit
        con.close()


def main():
    MainWindow.initDB(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

