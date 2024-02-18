import sys

# append the path of the parent directory
sys.path.append(".")

import csv
import datetime

path = "timeslots/Timeslots_v1.csv"

def readData():
    timeslotList = []
    with open(path, 'r') as timeslotData:
        reader = csv.reader(timeslotData, delimiter=";")
        next(reader)
        for i, row in enumerate(reader):
            starttime = datetime.datetime.strptime(row[0], '%H:%M:%S')
            endtime = starttime + datetime.timedelta(minutes=30)
            timeslot = Timeslot.Timeslot(i+1, starttime.time(), endtime.time(), row[1])
            timeslotList.append(timeslot)
    return timeslotList
