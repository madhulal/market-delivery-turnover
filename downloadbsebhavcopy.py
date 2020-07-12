from io import BytesIO
import urllib.request
from zipfile import ZipFile
import ssl
from datetime import datetime
from dateutil.relativedelta import relativedelta

def download_bse_bhavcopy(date, dir):
  day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % (abs(date.year)%100)
  ssl._create_default_https_context = ssl._create_unverified_context
  bhavurl = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_' + day + month + year+'.zip'
  page = urllib.request.Request(bhavurl,headers={'User-Agent': 'Mozilla/5.0'}) 
  print('Getting the BSE BHAV COPY named ' + bhavurl)
  with urllib.request.urlopen(page) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(dir)