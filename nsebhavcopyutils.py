from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
from mongoutils import insertrecord

monthtext={'01':'JAN','02':'FEB','03':'MAR','04':'APR','05':'MAY','06':'JUN','07':'JUL','08':'AUG','09':'SEP','10':'OCT','11':'NOV','12':'DEC'}

def getnsebhavcopy(date, dir):
  day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
  nsebhavzipurl = 'https://www1.nseindia.com/content/historical/EQUITIES/'+ year+'/'+ monthtext[month]+'cm'+day+monthtext[month]+year+'bhav.csv.zip'
  print('Getting the NSE BHAV COPY named ' + nsebhavzipurl)
  with urlopen(nsebhavzipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(dir)
  filename = 'cm'+day+monthtext[month]+year+'bhav.csv'
  storebhavcopy(dir, filename)

def storebhavcopy(dir, filename):
    print('Getting CSV: ' + dir + filename)
    file = open(dir+filename, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        print(dict(row))
    