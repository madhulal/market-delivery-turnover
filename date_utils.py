from datetime import datetime
from settings import DATE_FORMAT

today = datetime.today().date()


def is_weekend(date):
    weekno = date.weekday()
    if weekno >= 5:
        return True
    else:
        return False

# TODO Check the trading holidays


def is_trading_holiday(date):
    if(is_weekend(date)):
        return True
    else:
        return False


def format_date_string(date_string, input_format):
    return datetime.strptime(date_string, input_format).strftime(DATE_FORMAT)


def format_date(date):
    return date.strftime(DATE_FORMAT)
