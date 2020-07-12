from datetime import datetime

def is_weekend(date):
    weekno = date.weekday()
    if weekno >= 5:
        return True
    else: 
        return False

#TODO Check the trading holidays
def is_trading_holiday(date):
    if(is_weekend(date)):
        return True
    else:
        return False

today = datetime.today().date()
print(is_trading_holiday(today))