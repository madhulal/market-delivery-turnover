from io import BytesIO
import urllib.request
from zipfile import ZipFile
import ssl
from mongoutils import insertrecord
import csv

def getbsebhavcopy(date, dir):
  day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % (abs(date.year)%100)
  filename = 'EQ_ISINCODE_' + day + month + year+'.zip'
  ssl._create_default_https_context = ssl._create_unverified_context
  bhavurl = 'https://www.bseindia.com/download/BhavCopy/Equity/' + filename
  page = urllib.request.Request(bhavurl,headers={'User-Agent': 'Mozilla/5.0'}) 
  print('Getting the BSE BHAV COPY named ' + bhavurl)
  with urllib.request.urlopen(page) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(dir)
  updated_file_name = filename.replace("zip", "CSV")
  storebhavcopy(dir, updated_file_name)

def storebhavcopy(dir, file):
    print('Getting CSV: ' + dir + file)
    file = open(dir+file, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        print(rowdict)
        #rowdict["_id"] = rowdict["ISIN"] + "_" + rowdict["TIMESTAMP"]
        #del rowdict['']
         #insertrecord("bse_bhav_raw", rowdict)