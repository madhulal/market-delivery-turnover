import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient

monthtext={'01':'JAN','02':'FEB','03':'MAR','04':'APR','05':'MAY','06':'JUN','07':'JUL','08':'AUG','09':'SEP','10':'OCT','11':'NOV','12':'DEC'}

def store_nse_bhavcopy(date, dir):
  day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
  nsebhavcopyfile = dir + '/cm' + day + monthtext[month] + year + 'bhav.csv'
  print('Getting the file - ' + nsebhavcopyfile)
  csvfile = open(nsebhavcopyfile, 'r')
  reader = csv.DictReader( csvfile )
  mongo_client=MongoClient() 
  db=mongo_client.nse_bhav_copy
  header= [ "SYMBOL", "SERIES", "OPEN", "HIGH", "LOW", "CLOSE", "LAST", "PREVCLOSE", "TOTTRDQTY", "TOTTRDVAL", "TIMESTAMP", "TOTALTRADES", "ISIN"]
  for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.segment.insert(row)



