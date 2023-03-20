import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import pymysql

from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
from datetime import *

today = datetime.today().strftime("%Y%m%d") # 특수문자 제거
tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
day_after_tomorrow = (date.today() + timedelta(days=2)).strftime("%Y%m%d")

select_data_list = ['fcstDate', 'fcstTime', 'POP', 'PTY', 'REH', 'SKY', 'TMP', 'WSD']

class MainWindow(QtWidgets.QMainWindow):


    def __init__(self, *args, **kwargs):    
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('./seonghyeon_weatherApp/weatherApp.ui')
    #     self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])


    # def plot(self, hour, temperature):
    #     self.graphWidget.plot(hour, temperature)

    def initDB(self):
        con = pymysql.connect(
            host = '210.119.12.66', 	 #ex) '127.0.0.1' "210.119.12.66"
            port = 3306,
            user = "root", 		 #ex) root
            password = "12345",
            database = "miniproject01", 
            charset = 'utf8'
        )
        cur = con.cursor()
        item_list = []
        for item in range(len(select_data_list)):
            get_index_result = f'''SELECT {select_data_list[item]} 
                                     FROM parkseonghyeon
                                    WHERE (fcstDate = {today} and fcstTime = 1200) 
                                       or (fcstDate = {tomorrow} and fcstTime = 1200) 
                                       or (fcstDate = {day_after_tomorrow} and fcstTime = 1200);'''
            
            item_list.append(cur.execute(get_index_result))
            print(cur.fetchall())
        con.close()
        print(item_list)

def main():
    MainWindow.initDB(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

