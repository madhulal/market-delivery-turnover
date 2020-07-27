import csv
from download_utils import download_zip_file_mozilla_agent
from date_utils import format_date, format_date_string
from mongo_utils import insert_record, get_record, get_db, drop_collection
import logging
from datetime import date
from config import is_nse_fetch_enabled

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def drop_bse_collections():
    logger.warning('Clearing BSE collections')
    drop_collection("bse_bhav_raw")
    drop_collection("bse_delivery_raw")
    drop_collection("bse_combined")


def fetch_bse_data(date, dir):
    if(is_nse_fetch_enabled()):
        get_bse_bhav_copy(date, dir)
        get_bse_delivery_data(date, dir)
    else:
        logger.warning('BSE fetching is not enabled')


def get_bse_delivery_data(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    file_name = 'SCBSEALL' + day + month + '.zip'
    download_url = 'https://www.bseindia.com/BSEDATA/gross/' + year + '/' + file_name
    if(download_zip_file_mozilla_agent(download_url, dir)):
        updated_file_name = file_name.replace("zip", "TXT")
        store_delivery_data(dir, updated_file_name)


def get_bse_bhav_copy(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % (
        abs(date.year) % 100)
    filename = 'EQ_ISINCODE_' + day + month + year+'.zip'
    bhavurl = 'https://www.bseindia.com/download/BhavCopy/Equity/' + filename
    if(download_zip_file_mozilla_agent(bhavurl, dir)):
        extracted_file_name = filename.replace("zip", "CSV")
        store_bhav_copy(dir, extracted_file_name)
        return True


def store_bhav_copy(dir, file):
    logger.debug('Storing the data from {}'.format(file))
    file = open(dir+file, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        id = rowdict["ISIN_CODE"] + "_" + \
            rowdict["SC_TYPE"] + "_" + \
            format_date_string(rowdict["TRADING_DATE"], '%d-%b-%y')
        rowdict["_id"] = id
        logger.debug('Inserting BSE bhav copy data {} to DB'.format(rowdict))
        insert_record("bse_bhav_raw", rowdict)

        avg_trade_worth = float(rowdict["NET_TURNOV"]) / \
            int(rowdict["NO_TRADES"])
        avg_qty_per_trade = int(rowdict["NO_OF_SHRS"]) / \
            int(rowdict["NO_TRADES"])
        avg_price = float(rowdict["NET_TURNOV"]) / \
            int(rowdict["NO_OF_SHRS"])

        bse_combined_dict = {}
        bse_combined_dict["_id"] = id
        bse_combined_dict["isin"] = rowdict["ISIN_CODE"]
        bse_combined_dict["symbol"] = rowdict["SC_CODE"]
        bse_combined_dict["series"] = rowdict["SC_TYPE"]
        bse_combined_dict["date"] = format_date_string(
            rowdict["TRADING_DATE"], '%d-%b-%y')
        bse_combined_dict["volume"] = rowdict["NO_OF_SHRS"]
        bse_combined_dict["turnover"] = rowdict["NET_TURNOV"]
        bse_combined_dict["avg_trade_worth"] = avg_trade_worth
        bse_combined_dict["avg_quantity_per_trade"] = avg_qty_per_trade
        bse_combined_dict["avg_price"] = avg_price
        bse_combined_dict["delivery_turnover"] = 0.0
        logger.debug(
            'Inserting BSE bhav combined data {} to DB'.format(bse_combined_dict))
        insert_record("bse_combined", bse_combined_dict)

    logger.info('BSE bhav copy data is pushed to DB')


def store_delivery_data(dir, file_name):
    logger.debug("Storing the raw delivery data in DB from {file_name}")
    file = open(dir+file_name, 'r')
    csv_file = csv.DictReader(file, delimiter='|')
    for row in csv_file:
        rowdict = dict(row)
        symbol = rowdict["SCRIP CODE"]
        formatted_date = format_date_string(rowdict["DATE"], '%d%m%Y')
        delivery_percentage = rowdict["DELV. PER."]

        rowdict["_id"] = symbol + "_" + \
            formatted_date
        rowdict["DELIVERY PER"] = delivery_percentage
        del rowdict["DELV. PER."]

        logger.debug('Inserting BSE delivery data {} to DB'.format(rowdict))
        insert_record("bse_delivery_raw", rowdict)

        bse_combined_record = get_record(
            "bse_combined", {'symbol': symbol, 'date': formatted_date})
        delivery_turnover = float(rowdict["DELIVERY VAL"])
        new_val = {"delivery_turnover": delivery_turnover}
        logger.debug(
            'Updating BSE combined data {} to DB'.format(bse_combined_record))
        get_db().bse_combined.update_one(
            {"_id": bse_combined_record["_id"]},
            {"$set": new_val}, upsert=False)

    logger.info('BSE Delivery data is pushed to DB')


def test():
    request_date = date(2020, 7, 9)
    # drop_bse_collections()
    fetch_bse_data(request_date, '/tmp/market/bse/')


# test()
