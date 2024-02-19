import csv
import utils

import solutionPrinter as sp
import orToolsVRPTW as vrptw
import orToolsVRPTW_direct as direct

versionen = ['v2']

datasetName = 'dataset_1'

def getTimetableForVersion(customerList, version):
    for v in versionen:
        if v == version:
            vers = __import__(v)
    timetable = utils.createTimetable()
    for customer in customerList:
        timetable = vers.insertIntoTimetable(customer, timetable)
    return timetable


def excelAllVersions(versionenListe, customerList):
    for version, timetable in versionenListe.items():
        sp.excelTimetable(version, timetable, customerList, datasetName)


def orToolAllVersions(versionenListe):
    for version, timetable in versionenListe.items():
        print('Version {}:'.format(version))
        vrptw.solve(timetable)

def orToolAllVersionsdirect(versionenListe, customerList):
    for version, timetable in versionenListe.items():
       print('Version {}:'.format(version))
       direct.solve(customerList)


def main():

    versionenListe = {}
    for version in versionen:
        customerList = utils.createCustomerList()
        timetable = getTimetableForVersion(customerList, version)
        versionenListe[version] = timetable

    excelAllVersions(versionenListe, customerList)
    orToolAllVersions(versionenListe)
    #orToolAllVersionsdirect(versionenListe, customerList)

if __name__ == '__main__':
    main()
