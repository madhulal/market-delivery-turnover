from datetime import datetime
from dateutil.relativedelta import relativedelta
from nsebhavcopyutils import getnsebhavcopy
from bsebhavcopyutils import getbsebhavcopy
from settings import LOG_FILE, DATA_FOLDER
import os
from datetime import datetime
from holiday import istradingholiday

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
    if(istradingholiday(requestdate)):
        print('Holiday')
    else:
        getnsebhavcopy(requestdate, DATA_FOLDER)
        #getbsebhavcopy(requestdate, DATA_FOLDER)
        wr = requestdate.date()

# writing the last downloaded date to LOG file
if not isinstance(wr, str):
    logfile = open(LOG_FILE, 'w')
    # logfile.write(str(wr))
    logfile.close()
