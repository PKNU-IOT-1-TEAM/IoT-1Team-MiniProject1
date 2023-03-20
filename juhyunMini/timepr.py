# schedule
import schedule
import time

def sum():
    print('메롱')

schedule.every().day.at("21:32").do(sum)

while True:
        schedule.run_pending()

    
