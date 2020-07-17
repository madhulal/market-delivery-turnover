from datetime import datetime
from dateutil.relativedelta import relativedelta
from downloadnsebhavcopy import download_nse_bhavcopy
from downloadbsebhavcopy import download_bse_bhavcopy
from settings import LOG_FILE, DATA_FOLDER
import os
from datetime import datetime

today = datetime.today().date()
logfile = open(LOG_FILE, 'r')
lastdatestring = logfile.read(10)
logfile.close()

today = datetime.today().date()
lastdate = datetime.strptime(lastdatestring, '%Y-%m-%d')
diff, wr = today-lastdate.date(), ''
print(diff.days)

for i in range(1, diff.days+1):
    requestdate = lastdate + relativedelta(days=i)
    download_nse_bhavcopy(requestdate, DATA_FOLDER)
    download_bse_bhavcopy(requestdate, DATA_FOLDER)
    wr = requestdate.date()


# writing the last downloaded date to LOG file
if not isinstance(wr, str):
    logfile = open(LOG_FILE, 'w')
    logfile.write(str(wr))
    logfile.close()
