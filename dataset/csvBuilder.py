import csv
import datetime
from dataset import randomSetGenerator as rsg

def buildCsv(dataset):
    header = ["id", "xCoord", "yCoord", "custType", "delDate", "delTime", "willingToWait", "deliveryWindows", "priceSens"]
    timestamp = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-")
    filename = "dataset/dataSets_CSV/dataset_"+timestamp+".csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(header)
        for customer in dataset:
            writer.writerow(customer)

def createRandomCsvData(numberOfCustomers):
    buildCsv(rsg.getRandomDataset(numberOfCustomers))
