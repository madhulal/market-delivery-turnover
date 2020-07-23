#!/usr/bin/python3
from pymongo import MongoClient
from settings import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.marketdb


def get_db():
    return db


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


def get_record_by_id(collection, idvalue):
    record = db[collection].find_one({'_id': idvalue})
    return record


def get_record(collection, query):
    record = db[collection].find_one(query)
    return record


def print_records(collection):
    records = db[collection].find()
    for record in records:
        print(record)


def list_collections():
    print(db.collection_names())


def drop_collection(collection):
    db[collection].drop()


db_status()
list_collections()
""" count_records("nse_bhav_raw")
count_records("nse_delivery_raw")
count_records("nse_combined")
# print_records("nse_combined")
drop_collection("nse_bhav_raw")
drop_collection("nse_delivery_raw")
drop_collection("nse_combined")

count_records("bse_bhav_raw")
count_records("bse_delivery_raw")
count_records("bse_combined")

drop_collection("bse_bhav_raw")
drop_collection("bse_delivery_raw")
drop_collection("bse_combined") 

drop_collection("ichart_technical")
drop_collection("fundamental")"""
