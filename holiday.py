from datetime import datetime


def isweekend(date):
    weekno = date.weekday()
    if weekno >= 5:
        return True
    else:
        return False

# TODO Check the trading holidays
def istradingholiday(date):
    if(isweekend(date)):
        return True
    else:
        return False


today = datetime.today().date()
print(istradingholiday(today))
