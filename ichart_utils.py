import csv
from mongo_utils import insert_record
from download_utils import download_zip_file, download_file
from date_utils import format_date, format_date_string
import logging

logger = logging.getLogger(__name__)

def fetch_technical(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    file_name = 'ichart_' + format_date(date) + '.csv'
    download_url = 'https://www.icharts.in/includes/screener/EODScan.php?export=1'
    #download_file(download_url, dir, file_name)
    store_data(dir, file_name)


def store_data(dir, file_name):
    logger.debug("Storing the raw delivery data in DB from {file_name}")
    #clean_file(dir, file_name)
    file = open(dir+file_name, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["p_symbol"] + \
            "_" + format_date_string(rowdict["p_date"], '%Y-%m-%d')
        insert_record("ichart_technical", rowdict)