# 날씨 단기예보 GUI
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql  # MySQL DB 모듈

class qtApp(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('./FcstApp.ui', self)
        self.setWindowIcon(QIcon('./weather-forecast.png'))

        self.initDB()

    def initDB(self):
        conn = pymysql.connect(host='localhost', user = 'root', password='12345',
                               db = 'miniproject', charset='utf8')
        # 성현DB
        # conn = pymysql.connect(host='210.119.12.66', user = 'root', password='12345',
        #                     db = 'miniproject01', charset='utf8')

        cur = conn.cursor()
        query = '''SELECT Idx
	                    , fcstDate
                        , fcstTime
                        , TMP 
                        , VEC 
                        , WSD 
                        , SKY 
                        , PTY 
                        , POP 
                        , PCP 
                        , REH 
                        , SNO 
                        , TMN 
                        , TMM 
                     FROM weather'''      
        cur.execute(query)
        
        columns = cur.fetchall()
        # print(rows)
        self.makeTable(columns)

        conn.close()

    def makeTable(self, columns):
        self.tblWeather.setColumnCount(len(columns))
        self.tblWeather.setRowCount(8)
        self.tblWeather.setSelectionMode(QAbstractItemView.NoSelection)
        self.tblWeather.horizontalHeader().setVisible(False)
        self.tblWeather.setVerticalHeaderLabels(['시각', '날씨', '기온', '강수량(mm)'
                                                , '강수확률', '바람(m/s)', '습도', '한파영향'])
        
        for i, column in enumerate(columns):
            # Idx = column[0]   # 인덱스
            # fcstDate = column[1]  # 날짜
            fcstTime = column[2]    # 시각
            TMP = column[3] # 기온
            VEC = column[4] # 풍향
            WSD = column[5] # 풍속
            SKY = column[6] # 하늘상태
            PTY = column[7] # 강수형태
            POP = column[8] # 강수확률
            PCP = column[9] # 강수량
            REH = column[10]    # 습도
            SNO = column[11]    # 신적설
            # TMN = column[12]    # 최저 온도
            # TMM = column[13]    # 최고 온도

            self.tblWeather.setItem(0, i, QTableWidgetItem(str(fcstTime)))
            self.tblWeather.setItem(1, i, QTableWidgetItem(str(SKY)))
            self.tblWeather.setItem(2, i, QTableWidgetItem(str(TMP)))
            self.tblWeather.setItem(3, i, QTableWidgetItem(PCP))
            self.tblWeather.setItem(4, i, QTableWidgetItem(str(POP)))
            self.tblWeather.setItem(5, i, QTableWidgetItem(f'{VEC}, {WSD}'))
            self.tblWeather.setItem(6, i, QTableWidgetItem(str(REH)))
            self.tblWeather.setItem(7, i, QTableWidgetItem(str(SNO)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())