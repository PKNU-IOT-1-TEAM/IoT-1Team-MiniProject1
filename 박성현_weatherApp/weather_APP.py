import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic


form_class = uic.loadUi('./IoT-1Team-MiniProject1/seonghyeon_weatherApp/weatherApp.ui')

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        y = [4, 7, 9,10]
        self.graphicsView.addLegend(size=(140, 40)) ## 범례
        self.graphicsView.plot(y, title='Plot test', name='Legend name', pen='r', symbol='o', symbolPen='g', symbolBrush=0.2)
        self.graphicsView.showGrid(x=True, y=True) #그리드 표현
        self.graphicsView.setTitle(title='Title name')

def main():
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

if __name__ == "__main__":
    main()