import csv
from mongo_utils import insert_record, drop_collection
from download_utils import download_zip_file, download_file
from date_utils import format_date, format_date_string
import logging
from datetime import date
from config import is_technical_enabled

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def drop_collections():
    logger.warning('Clearing Technical collections')
    drop_collection("ichart_technical")


def fetch_technical(date, dir):
    if(is_technical_enabled()):
        day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
        file_name = 'ichart_' + format_date(date) + '.csv'
        download_url = 'https://www.icharts.in/includes/screener/EODScan.php?export=1'
        download_file(download_url, dir, file_name)
        store_data(dir, file_name)
    else:
        logger.warning('iChart fetching not enabled')


def store_data(dir, file_name):
    logger.debug("Storing the technical data in DB from {}".format(file_name))
    file = open(dir+file_name, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["p_symbol"] + \
            "_" + format_date_string(rowdict["p_date"], '%Y-%m-%d')
        insert_record("ichart_technical", rowdict)
    logger.info('Technical data is pushed to DB')


def test():
    request_date = date(2020, 7, 9)
    # drop_collections()
    fetch_technical(request_date, '/tmp/market/technical/')


# test()
