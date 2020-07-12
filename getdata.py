from datetime import datetime
from dateutil.relativedelta import relativedelta
from downloadnsebhavcopy import download_nse_bhavcopy
from storensebhavcopy import store_nse_bhavcopy
from downloadbsebhavcopy import download_bse_bhavcopy

datadir = '/tmp/market/bhav'
today = datetime.today().date()
requestdate = today - relativedelta(days=2)
#Download nse bhav copy
download_nse_bhavcopy(requestdate, datadir)
#store_nse_bhavcopy(requestdate, datadir)

download_bse_bhavcopy(requestdate, datadir)