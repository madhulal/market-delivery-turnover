from datetime import datetime
from dateutil.relativedelta import relativedelta
from nse_utils import fetch_nse_data, drop_nse_collections
from bse_utils import fetch_bse_data, drop_bse_collections
from ichart_utils import fetch_technical
from fundamental_utils import fetch_fundamentals
from settings import LOG_FILE, DATA_FOLDER, FUNDAMENTALS_FILE_NAME
import os
from datetime import datetime
from date_utils import is_trading_holiday
import logging

logger = logging.getLogger(__name__)

# TODO Get it from DB
logfile = open(LOG_FILE, 'r')
lastdatestring = logfile.read(10)
logfile.close()
#lastdatestring = '2020-07-16'

today = datetime.today().date()
lastdate = datetime.strptime(lastdatestring, '%Y-%m-%d')
diff, wr = today-lastdate.date(), ''
logger.info('Updating data for last {} days'.format(diff.days))


fetch_fundamentals(datetime.today())
fetch_technical(datetime.today(), DATA_FOLDER)

# drop_nse_collections()
# drop_bse_collections()

for i in range(1, diff.days+1):
    requestdate = lastdate + relativedelta(days=i)
    if(is_trading_holiday(requestdate)):
        logger.info('{} is a trading holiday'.format(requestdate))
    else:
        fetch_nse_data(requestdate, DATA_FOLDER + "nse/")
        fetch_bse_data(requestdate, DATA_FOLDER + "bse/")
        wr = requestdate.date()
# writing the last downloaded date to LOG file
if not isinstance(wr, str):

    #logfile = open(LOG_FILE, 'w')
    # logfile.write(str(wr))
    # logfile.close()
    print("TODO update the last processed date")
