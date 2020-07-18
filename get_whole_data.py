from datetime import datetime
from dateutil.relativedelta import relativedelta
from nse_bhav_copy_utils import get_nse_bhav_copy, get_nse_delivery_data
from bse_bhav_copy_utils import get_bse_bhav_copy
from settings import LOG_FILE, DATA_FOLDER
import os
from datetime import datetime
from date_utils import is_trading_holiday


logfile = open(LOG_FILE, 'r')
lastdatestring = logfile.read(10)
logfile.close()

today = datetime.today().date()
lastdate = datetime.strptime(lastdatestring, '%Y-%m-%d')
diff, wr = today-lastdate.date(), ''
print('Updating data for last {} days'.format(diff.days))

for i in range(1, diff.days+1):
    requestdate = lastdate + relativedelta(days=i)
    if(is_trading_holiday(requestdate)):
        print("{} is a trading holiday".format(requestdate))
    else:
        #get_nse_bhav_copy(requestdate, DATA_FOLDER)
        #get_bse_bhav_copy(requestdate, DATA_FOLDER)
        get_nse_delivery_data(requestdate, DATA_FOLDER)
        wr = requestdate.date()

# writing the last downloaded date to LOG file
if not isinstance(wr, str):
    #logfile = open(LOG_FILE, 'w')
    # logfile.write(str(wr))
    # logfile.close()
    print("TODO update the last processed date")
