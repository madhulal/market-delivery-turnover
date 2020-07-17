from settings import LOG_FILE
import os
from datetime import datetime

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w'):
        pass

logfile = open(LOG_FILE, 'r')
lastdt = logfile.read(10)
logfile.close()
today = datetime.today().date()
print(lastdt)
lastdt = datetime.strptime(lastdt, '%Y-%m-%d')
diff, wr = today-lastdt.date(), ''
print(diff, wr)
