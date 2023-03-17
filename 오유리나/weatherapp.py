import sys 
import pymysql
from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
 
class qtApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI, ICON, Title
        uic.loadUi('./오유리나/weather.ui', self)
        self.setWindowIcon(QIcon('./오유리나/image/icon.png'))
        self.setWindowTitle('How is the weather?')

        self.lbl.setPixmap(QPixmap("./오유리나/image/now.png"))
                #라벨 생성
        
        label1 = QLabel(self)
        label1.move(10,10)
 
        #이미지 관련 클래스 생성 및 이미지 불러오기 
        pixmap = QPixmap('./오유리나/image/now.png')
        #이미지 관련 클래스와 라벨 연결 
        label1.setPixmap(pixmap)
        self.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())