#!/usr/bin/python3
from pymongo import MongoClient
from settings import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.marketdb


def insertrecord(collection, record):
    db[collection].insert(record)


def insertrecords(collection, records):
    db[collection].insert_many(records)


def printrecords(collection):
    records = db[collection].find()
    for record in records:
        print(record)


def listcollections():
    print(db.collection_names())


def dropcollection(collection):
    db[collection].drop()


cars = [{'_id': 123, 'name': 'Audi', 'price': 52642},
        {'name': 'Mercedes', 'price': 57127},
        {'name': 'Skoda', 'price': 9000},
        {'name': 'Volvo', 'price': 29000},
        {'name': 'Bentley', 'price': 350000},
        {'name': 'Citroen', 'price': 21000},
        {'name': 'Hummer', 'price': 41400},
        {'name': 'Volkswagen', 'price': 21600}]
# dropcollection("car")
#insertrecord("car", cars)
# listcollections()
# printrecords("car")
