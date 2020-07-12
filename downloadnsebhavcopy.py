from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from datetime import datetime
from dateutil.relativedelta import relativedelta

monthtext={'01':'JAN','02':'FEB','03':'MAR','04':'APR','05':'MAY','06':'JUN','07':'JUL','08':'AUG','09':'SEP','10':'OCT','11':'NOV','12':'DEC'}

def download_nse_bhavcopy(date, dir):
  day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
  nsebhavzipurl = 'https://www1.nseindia.com/content/historical/EQUITIES/'+ year+'/'+ monthtext[month]+'/cm'+day+monthtext[month]+year+'bhav.csv.zip'
  print('Getting the file - ' + nsebhavzipurl)
  with urlopen(nsebhavzipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(dir)