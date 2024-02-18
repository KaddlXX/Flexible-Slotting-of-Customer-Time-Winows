import random
import datetime
import csv

customerTypes = ["Stay-at-Home", "Senior", "Student", "Business"]   #types of customers

def getRandomDeliveryTimeForCustomerType(customerType):
    minutes = str(random.choice([0, 30])) # minutes is a random choice between 0 and 30 minutes
    if customerType == "Stay-at-Home":
        daytime = random.choice(["late-morning", "late-afternoon"])
        if daytime == "late-morning":
            if minutes == 0:
                hours = str(random.randint(9, 12))
            else:
                hours = str(random.randint(8, 11))
        else:
            if minutes == 0:
                hours = str(random.randint(14, 18))
            else:
                hours = str(random.randint(14, 17))
    elif customerType == "Senior":
        if minutes == 0:
            hours = str(random.randint(6, 15))
        else:
            hours = str(random.randint(6, 14))
    elif customerType == "Student":
        if minutes == 0:
            hours = str(random.randint(11, 22))
        else:
            hours = str(random.randint(11, 21))
    else:
        daytime = random.choice(["morning", "evening"])
        if daytime == "morning":
            if minutes == 0:
                hours = str(random.randint(6, 8))
            else:
                hours = str(random.randint(6, 7))
        else:
            if minutes == 0:
                hours = str(random.randint(20, 22))
            else:
                hours = str(random.randint(20, 21))
    timeString = hours+"::"+minutes
    time = datetime.datetime.strptime(timeString, "%H::%M").time()
    return time

def getDeliveryWindowOnCustomerType(customerType):
    match customerType:
        case "Stay-at-Home":
            window = "[[9:00:00, 12:00:00], [14:00:00, 18:00:00]]"
        case "Senior":
            window = "[[6:00:00, 17:00:00]]"
        case "Student":
            window = "[[11:00:00, 22:00:00]]"
        case "Business":
            window = "[[6:00:00, 8:00:00], [20:00:00, 22:00:00]]"
    return window

def getRandomDataset(numberOfCustomers):
    dataset = []
    for x in range(numberOfCustomers):
        customer = []
        id = x+1
        xCoord = random.randint(1, 20)    # random number between 1 and 20
        yCoord = random.randint(1, 20)    # random number between 1 and 20
        cust = random.choice(customerTypes)
        date = datetime.date.today() + datetime.timedelta(days=1)   # the date on which the customer wants his order delivered is always 1 day in the future
        time = getRandomDeliveryTimeForCustomerType(cust)
        if cust == "Business":
            willingToWait = False
        else:
            willingToWait = random.choice([True, False])
        if willingToWait:
            deliveryWindows = getDeliveryWindowOnCustomerType(cust)
        else:
            deliveryWindows = []
        if cust == "Senior":
            price = True
        elif cust == "Business":
            price = False
        else:
            price = random.choice([True, False])
        customer.extend((id, xCoord, yCoord, cust, date, time, willingToWait, deliveryWindows, price))
        dataset.append(customer)
    return dataset
