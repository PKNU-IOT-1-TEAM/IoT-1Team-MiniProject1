from weather_API import *

def main():
    # weather_Logic 객체 생성
    weatherlogic = weather_Logic()
    # weatherlogic 내부 함수 Short_term_checkDate 사용
    weatherlogic.Short_term_checkDate()
    # 시스템 시간 가져오기
    MainWindow.initDB(sys.argv)
    # app 객체 생성
    app = QtWidgets.QApplication(sys.argv)
    # main 객체 생성
    main = MainWindow()
    # 보여주기
    main.show()
    # 종료
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

