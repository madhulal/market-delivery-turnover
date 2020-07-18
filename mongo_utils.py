#!/usr/bin/python3
from pymongo import MongoClient
from settings import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.marketdb


def db_status():
    print(db.collection_names())
    status = db.command("dbstats")
    print(status)


def count_records(collection):
    n_records = db[collection].find().count()
    print("There are {} records".format(n_records))


def insert_record(collection, record):
    db[collection].insert(record)


def insert_records(collection, records):
    db[collection].insert_many(records)


def update_record(collection, record):
    db[collection].update_one(record, upsert=True)


def get_record(collection, idvalue):
    record = db[collection].find_one({'_id': idvalue})
    return record


def print_records(collection):
    records = db[collection].find()
    for record in records:
        print(record)


def list_collections():
    print(db.collection_names())


def drop_collection(collection):
    db[collection].drop()


cars = [{'_id': 123, 'name': 'Audi', 'price': 52642},
        {'name': 'Mercedes', 'price': 57127},
        {'name': 'Skoda', 'price': 9000},
        {'name': 'Volvo', 'price': 29000},
        {'name': 'Bentley', 'price': 350000},
        {'name': 'Citroen', 'price': 21000},
        {'name': 'Hummer', 'price': 41400},
        {'name': 'Volkswagen', 'price': 21600}]

# drop_collection("car")
# insert_record("car", cars)
# list_collections()
# print_records("car")

# db_status()
# count_records("nse_bhav_raw")

# drop_collection("nse_bhav_raw")
