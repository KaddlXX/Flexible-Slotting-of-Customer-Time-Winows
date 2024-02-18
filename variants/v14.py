import datetime

import utils

def resetTimetable(timetable):
    for slot in timetable:
        if len(slot.customerList) == 0:
            slot.isFree = True
        else:
            slot.isFree = False
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


def insertIntoTimetable(customer, timetable): #needed for every variation
    print(f"INFO: Customer {customer.id} operating order!!")
    timetable = timetable
    slot = getMostSuitableSlot(customer, timetable)
    if slot:
        customer.satisfaction = "Very Satisfied"
        customer.sReason = "Suitable Slot"
        customer.orderPrice = slot.price
        slot.customerList.append(customer)
        print(f"INFO: Customer {customer.id} got suitable slot.")
    else:
        customer.satisfaction = "Very Dissatisfied"
        customer.sReason = "Willing to change, but no Slot available"
        print(f"INFO: Customer {customer.id} was  willing to change, but no Slot was available.")

    timetable = resetTimetable(timetable)
    return timetable
