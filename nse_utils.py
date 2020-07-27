import csv
from mongo_utils import insert_record, get_record, get_db, drop_collection
from download_utils import download_zip_file, download_file
from date_utils import format_date, format_date_string
import logging
from datetime import date
from config import is_nse_fetch_enabled

monthtext = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN',
             '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def drop_nse_collections():
    logger.warning('Clearing NSE collections')
    drop_collection("nse_bhav_raw")
    drop_collection("nse_delivery_raw")
    drop_collection("nse_combined")


def fetch_nse_data(date, dir):
    if(is_nse_fetch_enabled()):
        get_nse_bhav_copy(date, dir)
        get_nse_delivery_data(date, dir)
    else:
        logger.warning('NSE fetching is not enabled')


def get_nse_delivery_data(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    file_name = 'MTO_' + day + month + year + '.DAT'
    download_url = 'https://www1.nseindia.com/archives/equities/mto/' + file_name
    if(download_file(download_url, dir, file_name)):
        store_delivery_data(dir, file_name, date)


def get_nse_bhav_copy(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    file_name = 'cm'+day+monthtext[month]+year+'bhav.csv'
    nsebhavzipurl = 'https://www1.nseindia.com/content/historical/EQUITIES/' + \
        year+'/' + monthtext[month]+'/' + file_name+'.zip'

    if(download_zip_file(nsebhavzipurl, dir)):
        store_bhav_copy(dir, file_name)


def store_bhav_copy(dir, file_name):
    logger.debug('Storing the NSE raw bhav copy from {file_name}')
    file = open(dir+file_name, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        id = rowdict["ISIN"] + "_" + \
            rowdict["SERIES"] + "_" + \
            format_date_string(rowdict["TIMESTAMP"], '%d-%b-%Y')
        rowdict["_id"] = id
        del rowdict['']
        logger.debug('Inserting NSE bhav copy data {} to DB'.format(rowdict))
        insert_record("nse_bhav_raw", rowdict)

        avg_trade_worth = float(rowdict["TOTTRDVAL"]) / \
            int(rowdict["TOTALTRADES"])
        avg_qty_per_trade = int(rowdict["TOTTRDQTY"]) / \
            int(rowdict["TOTALTRADES"])
        avg_price = float(rowdict["TOTTRDVAL"]) / \
            int(rowdict["TOTTRDQTY"])

        nse_combined_dict = {}
        nse_combined_dict["_id"] = id
        nse_combined_dict["isin"] = rowdict["ISIN"]
        nse_combined_dict["symbol"] = rowdict["SYMBOL"]
        nse_combined_dict["series"] = rowdict["SERIES"]
        nse_combined_dict["date"] = format_date_string(
            rowdict["TIMESTAMP"], '%d-%b-%Y')
        nse_combined_dict["close_price"] = rowdict["CLOSE"]
        nse_combined_dict["volume"] = rowdict["TOTTRDQTY"]
        nse_combined_dict["turnover"] = rowdict["TOTTRDVAL"]
        nse_combined_dict["avg_trade_worth"] = avg_trade_worth
        nse_combined_dict["avg_quantity_per_trade"] = avg_qty_per_trade
        nse_combined_dict["avg_price"] = avg_price
        nse_combined_dict["delivery_turnover"] = 0.0
        logger.debug(
            'Inserting NSE bhav combined data {} to DB'.format(nse_combined_dict))
        insert_record("nse_combined", nse_combined_dict)

    logger.info('NSE bhav copy data is pushed to DB')


def update_delivery_file_header(content):
    # Adding Series header
    content = content.replace(
        'Name of Security,Quantity Traded', 'Name of Security,Series,Quantity Traded')
    # Changing the header to more readable
    content = content.replace(
        'Deliverable Quantity(gross across client level),% of Deliverable Quantity to Traded Quantity',
        'Deliverable Quantity,Percentage of Delivery')
    return content


def store_delivery_data(dir, file_name, date):
    logger.debug("Storing the NSE raw delivery data in DB from {file_name}")

    # The file needs to be excluded first three lines; also missed the series column
    with open(dir + file_name) as f:
        lines_after_3 = f.readlines()[3:]
        f.close

    lines_after_3[0] = update_delivery_file_header(lines_after_3[0])

    new_file = open(dir + file_name + '.csv', 'w')
    new_file.writelines(lines_after_3)
    new_file.close

    file = open(new_file.name, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        symbol = rowdict["Name of Security"]
        series = rowdict["Series"]
        formatted_date = format_date(date)
        rowdict["_id"] = symbol + "_" + \
            series + "_" + \
            formatted_date
        del rowdict['Record Type']
        del rowdict['Sr No']
        logger.debug(
            'Inserting raw NSE delivery data {} to DB'.format(rowdict))
        insert_record("nse_delivery_raw", rowdict)

        nse_combined_record = get_record(
            "nse_combined", {'symbol': symbol, 'series': series, 'date': formatted_date})
        avg_price = nse_combined_record['avg_price']
        delivery_turnover = avg_price * \
            int(rowdict["Deliverable Quantity"])
        new_val = {"delivery_turnover": delivery_turnover}
        logger.debug(
            'Updating NSE combined data {} to DB'.format(nse_combined_record))
        get_db().nse_combined.update_one(
            {"_id": nse_combined_record["_id"]},
            {"$set": new_val}, upsert=False)

    logger.info('NSE delivery data is pushed to DB')


def test():
    request_date = date(2020, 7, 9)
    # drop_nse_collections()
    fetch_nse_data(request_date, '/tmp/market/nse/')


test()
