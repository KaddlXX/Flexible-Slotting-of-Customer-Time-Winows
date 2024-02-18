import utils
import csv

def rejectionResults(customerList, timetable):
    for customer in customerList:
        res = any(customer in slot.customerList for slot in timetable)
        if not res:
            print(f" {customer.id};{customer.xCoord};{customer.yCoord};{customer.custType};{customer.satisfaction};{customer.sReason};{customer.time};{customer.willingToWait}")

def prettyPrintTimetable(timetable):
    for slot in timetable:
        if slot.customerList:
            for customer in slot.customerList:
                print(f" {customer.id};{customer.xCoord};{customer.yCoord};{customer.custType};{customer.satisfaction};{customer.sReason};{customer.time};{customer.willingToWait};{slot.id};{slot.start} - {slot.end}")
            if len(slot.customerList) > 1:
                distance = utils.calculateDistance((slot.customerList[0].xCoord, slot.customerList[0].yCoord), (slot.customerList[1].xCoord, slot.customerList[1].yCoord))
                print(f"Distance {distance}")
            #print("\n")


def excelTimetable(version, timetable, cstmList, datasetName):
    header = ["CustomerId", "Xcoord", "Ycoord", "CustomerType", "SatisfactionStatus", "ReasonForSatisfaction", "PreferredTimeSlot", "WillingnessToChangeTS", "TimeslotId", "TimeslotStart", "TimeslotEnd", "OrderPrice"]
    filename = 'excelOutput/excelOutput_'+version+'_'+datasetName+'.csv'
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)
        for customer in cstmList:
            accepted = False
            for slot in timetable:
                for cust in slot.customerList:
                    if cust.id == customer.id:
                        writer.writerow([customer.id, customer.xCoord, customer.yCoord, customer.custType, customer.satisfaction, customer.sReason, customer.time, customer.willingToWait, slot.id, slot.start, slot.end, customer.orderPrice])
                        accepted = True
            if not accepted:
                writer.writerow([customer.id, customer.xCoord, customer.yCoord, customer.custType, customer.satisfaction, customer.sReason, customer.time, customer.willingToWait, None, None, None, None])
                accepted = False
