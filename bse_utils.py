import csv
from download_utils import download_zip_file_mozilla_agent
from date_utils import format_date, format_date_string
from mongo_utils import insert_record
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


def store_bhav_copy(dir, file):
    logger.debug('Storing the data from {}'.format(file))
    file = open(dir+file, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["ISIN_CODE"] + \
            "_" + format_date_string(rowdict["TRADING_DATE"], '%d-%b-%y')
        logger.debug('Inserting BSE bhav copy data {rowdict} to DB')
        logger.debug(rowdict)
        insert_record("bse_bhav_raw", rowdict)
    logger.info('BSE bhav copy data is pushed to DB')


def store_delivery_data(dir, file_name):
    logger.debug("Storing the raw delivery data in DB from {file_name}")
    file = open(dir+file_name, 'r')
    csv_file = csv.DictReader(file, delimiter='|')
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["SCRIP CODE"] + "_" + \
            format_date_string(rowdict["DATE"], '%d%m%Y')
        logger.debug('Inserting BSE delivery data {rowdict} to DB')
        insert_record("bse_delivery_raw", rowdict)
    logger.info('BSE Delivery data is pushed to DB')
