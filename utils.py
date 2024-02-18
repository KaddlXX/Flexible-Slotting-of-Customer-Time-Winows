import csv
import glob
import datetime
import math

import Customer
import Timeslot

# function to create a List of Timeslots given a optional path to csv file.
def createTimetable(pathToTimeslotCsv='timeslots/Timeslots_v1.csv'):
    timeslotList = []
    with open(pathToTimeslotCsv, 'r') as timeslotData:
        reader = csv.reader(timeslotData, delimiter=';')
        next(reader)
        for i, row in enumerate(reader):
            starttime = datetime.datetime.strptime(row[0], '%H:%M:%S')
            endtime = starttime + datetime.timedelta(minutes=30) # timeslots are 30 minutes long
            timeslot = Timeslot.Timeslot(i+1, starttime.time(), endtime.time(), row[1])
            timeslotList.append(timeslot)
    return timeslotList

# function to create a List of Customers given a optional path to csv file.
def createCustomerList(pathToCustomerCsv='dataset/dataSets_CSV/import/*.csv'):
    customerList = []
    path = glob.glob(pathToCustomerCsv)
    with open(path[0], 'r') as customerData:
        reader = csv.reader(customerData, delimiter=';')
        next(reader)
        for row in reader:
            id = int(row[0])
            xCoord = int(row[1])
            yCoord = int(row[2])
            custType = str(row[3])
            date = datetime.datetime.strptime(row[4], '%Y-%m-%d').date()
            time = datetime.datetime.strptime(row[5], '%H:%M:%S').time()
            willingToWait = eval(row[6])
            if willingToWait:
                deliveryWindows = [[datetime.datetime.strptime(i, '%H:%M:%S').time() for i in x.strip(" []").split(", ")] for x in row[7].strip('[]').split("],")]
            else:
                deliveryWindows = []
            priceSens = eval(row[8])
            customer = Customer.Customer(id, xCoord, yCoord, custType, date, time, willingToWait, deliveryWindows, priceSens)
            customerList.append(customer)
    return customerList

# function to calculate the euclidean distance between two points (x,y) and corrected with factor 1.5 for Roadnetwork (Ehmke et al. 2014)
def calculateDistance(xy1, xy2):
    dist = (math.sqrt(((xy2[0] - xy1[0]) ** 2 + (xy2[1] - xy1[1]) ** 2)))*1.5
    return dist

