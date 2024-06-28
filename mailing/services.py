from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def hello():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(hello, 'interval', seconds=10)
    scheduler.start()
