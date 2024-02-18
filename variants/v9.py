import datetime

import utils

def resetTimetable(timetable):
    for slot in timetable:
        if len(slot.customerList) == 0:
            slot.isFree = True
        else:
            slot.isFree = False
        if slot.price == 'cheap':
            slot.price = 'normal'
    return timetable

def getSlotLength(slot):
    date = datetime.date(1, 1, 1)
    start = datetime.datetime.combine(date, slot.start)
    end = datetime.datetime.combine(date, slot.end)
    slotLength = end - start
    return slotLength

def getDiffTime(datetime1, datetime2):
    if datetime1 < datetime2:
        delta = datetime2-datetime1
    else:
        delta = datetime1-datetime2
    return delta

def getMostSuitableSlot(customer, timetable):
    print(f"INFO: Get mostSuitableSlot for Customer {customer.id}.")
    mostSuitableSlot = []
    for window in customer.deliveryWindows:
        for slot in timetable:
            if window[0] <= slot.start and window[1] >= slot.end:
                if slot.isFree:
                    datetimeSlot = datetime.datetime.combine(customer.date, slot.start)
                    datetimeCust = datetime.datetime.combine(customer.date, customer.time)
                    diffToSlot = getDiffTime(datetimeSlot, datetimeCust)
                    if mostSuitableSlot:
                        dateTimeMostSuit = datetime.datetime.combine(customer.date, mostSuitableSlot.start)
                        diffToMostSuit = getDiffTime(dateTimeMostSuit, datetimeCust)
                        if diffToSlot < diffToMostSuit:
                            mostSuitableSlot = slot
                    else:
                        mostSuitableSlot = slot
    return mostSuitableSlot

def getCheapestSlot(customer, timetable):
    print(f"INFO: Get cheapestSlot for Customer {customer.id}.")
    cheapestSlot = []
    for window in customer.deliveryWindows:
        for slot in timetable:
            if window[0] <= slot.start and window[1] >= slot.end:
                if slot.isFree:
                    datetimeSlot = datetime.datetime.combine(customer.date, slot.start)
                    datetimeCust = datetime.datetime.combine(customer.date, customer.time)
                    diffToSlot = getDiffTime(datetimeSlot, datetimeCust)
                    if cheapestSlot:
                        dateTimeCheapest = datetime.datetime.combine(customer.date, cheapestSlot.start)
                        diffToCheapest = getDiffTime(dateTimeCheapest, datetimeCust)
                        if diffToSlot < diffToCheapest:
                            if (slot.price == "cheap") or (slot.price == "normal" and cheapestSlot.price != "cheap") or (slot.price == "expensive" and cheapestSlot.price == "expensive"):
                                cheapestSlot = slot
                    else:
                        cheapestSlot = slot

    return cheapestSlot

def insertIntoTimetable(customer, timetable): #needed for every variation
    print(f"INFO: Customer {customer.id} operating order!!")
    timetable = timetable
    preferredSlot = [slot for slot in timetable if slot.start == customer.time][0]
    if preferredSlot.isFree:
        if customer.priceSens:
            if preferredSlot.price == "cheap":  # Is the preferred time slot price cheap? Yes
                print(f"INFO: Customer {customer.id} got a cheap slot.")
                customer.sReason = "Preferred cheap Slot"
                customer.orderPrice = preferredSlot.price
                preferredSlot.customerList.append(customer)
            elif preferredSlot.price == "normal":
                print(f"INFO: Customer {customer.id} got cheapest possible slot.")
                customer.satisfaction = "Satisfied"
                customer.sReason = "Preferred cheapest Slot"
                customer.orderPrice = preferredSlot.price
                preferredSlot.customerList.append(customer)
            else:
                customer.satisfaction = "Dissatisfied"
                customer.sReason = "Not willing to change and canceled order"
                print(f"INFO: Customer {customer.id} was not willing to wait and canceled the order.")
        else:
            customer.sReason = "Preferred Slot"
            customer.orderPrice = preferredSlot.price
            preferredSlot.customerList.append(customer)
            print(f"INFO: Customer {customer.id} got its preferred slot.")
    else:
        customer.satisfaction = "Dissatisfied"
        customer.sReason = "Not willing to wait and canceled order"
        print(f"INFO: Customer {customer.id} was not willing to wait and canceled the order.")
    timetable = resetTimetable(timetable)
    return timetable
