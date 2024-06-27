import lookup
from models import Offer,Task
from sqlalchemy.orm import Session
from engine import engine
import threading
import datetime
import time as sleep

taskdays = {}

def run():
    lookup.getlinks()
    lookup.runinfo()
    lookup.getbadlinks()
    lookup.runinfo()

def watcher():
    global taskdays
    while True:
        if str(datetime.datetime.today().date()) not in taskdays:
                        taskdays[str(datetime.datetime.today().date())] = []
        with Session(engine) as session:
            for task in session.query(Task).all():
                weekday = int(task.weekday)
                today = datetime.datetime.today().weekday()
                time = datetime.datetime.strptime(str(task.time),'%H:%M')
                now =  datetime.datetime.strptime(datetime.datetime.today().strftime('%H:%M'),'%H:%M')
                delta = time - now
                delta = delta.total_seconds()
                
                if delta <= 0 and (today == weekday or weekday == 7) and (weekday not in taskdays[str(datetime.datetime.today().date())] and time not in taskdays[str(datetime.datetime.today().date())]):
                    taskdays[str(datetime.datetime.today().date())].append([weekday,time])
                    run()
        sleep.sleep(15)
                    
if __name__ == "__main__":
    threading.Thread(target=lookup.getports).start()
    watcher()