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
    if datetime1 <= datetime2:
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

def createSpecificTimetable(customer, timetable):
    for slot in timetable:
        if slot.customerList and len(slot.customerList) < 2:
            distance = utils.calculateDistance((slot.customerList[0].xCoord, slot.customerList[0].yCoord), (customer.xCoord, customer.yCoord))
            if distance <= 3:
                slot.isFree = True
                slot.price = "cheap"
                index = timetable.index(slot)
                if timetable[index-1]:
                    timetable[index-1].price = "cheap"
                if timetable[index+1]:
                    timetable[index+1].price = "cheap"
    return timetable

def insertIntoTimetable(customer, timetable):
    print(f"INFO: Customer {customer.id} operating order!!")
    timetable = createSpecificTimetable(customer, timetable)
    preferredSlot = [slot for slot in timetable if slot.start == customer.time][0]
    if preferredSlot.isFree:
        if customer.priceSens:
            if preferredSlot.price == "cheap":
                print(f"INFO: Customer {customer.id} got a cheap slot.")
                customer.sReason = "Preferred cheap Slot"
                customer.orderPrice = preferredSlot.price
                preferredSlot.customerList.append(customer)
            elif preferredSlot.price == "normal":
                print(f"INFO: Customer {customer.id} got cheapest possible slot.")
                customer.satisfaction = "Very Satisfied"
                customer.sReason = "Preferred cheapest Slot"
                customer.orderPrice = preferredSlot.price
                preferredSlot.customerList.append(customer)
            elif customer.willingToWait:
                slot = getCheapestSlot(customer, timetable)  # Offers cheapest possible slot to customer
                if slot:
                    customer.satisfaction = "Satisfied"
                    customer.sReason = "Cheapest possible Slot"
                    customer.orderPrice = slot.price
                    slot.customerList.append(customer)
                    print(f"INFO: Customer {customer.id} got not the preferred slot, but another cheap slot.")
                else:  # No cheap slot available, but customer wolling to wait
                    customer.satisfaction = "Very Dissatisfied"
                    customer.sReason = "No Cheap Slot, but customer was willing to change"
                    print("WARNING: There is no free cheap slot left for Customer ")
            else:
                customer.satisfaction = "Dissatisfied"
                customer.sReason = "Not willing to change and canceled order"
                print(f"INFO: Customer {customer.id} was not willing to change and canceled the order.")
        else:
            print(f"INFO: Customer {customer.id} got its preferred slot.")
            customer.sReason = "Preferred Slot"
            customer.orderPrice = preferredSlot.price
            preferredSlot.customerList.append(customer)
    elif customer.willingToWait:
        if customer.priceSens:
            slot = getCheapestSlot(customer, timetable) #Offers cheapest possible slot to customer
            if slot:
                customer.satisfaction = "Satisfied"
                customer.sReason = "Cheapest possible Slot"
                customer.orderPrice = slot.price
                slot.customerList.append(customer)
                print(f"INFO: Customer {customer.id} got not the preferred slot, but another cheap slot.")
            else: #No cheap slot available, but customer wolling to wait
                customer.satisfaction = "Very Dissatisfied"
                customer.sReason = "No Cheap Slot, but customer was willing to change"
                print("WARNING: There is no free cheap slot left for Customer "+str(customer.id)+" and its time window ".join(f"{window[0]} - {window[1]} " for window in customer.deliveryWindows))
        else:
            slot = getMostSuitableSlot(customer, timetable)
            if slot:
                customer.satisfaction = "Satisfied"
                customer.sReason = "Suitable Slot"
                customer.orderPrice = slot.price
                slot.customerList.append(customer)
                print(f"INFO: Customer {customer.id} got suitable slot.")
            else:
                customer.satisfaction = "Very Dissatisfied"
                customer.sReason = "Willing to change, but no Slot available"
                print(f"INFO: Customer {customer.id} was  willing to change, but no Slot was available.")

    else:
        customer.satisfaction = "Dissatisfied"
        customer.sReason = "Not willing to change and canceled order"
        print(f"INFO: Customer {customer.id} was not willing to change and canceled the order.")
    timetable = resetTimetable(timetable)
    return timetable