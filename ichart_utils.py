import csv
from mongo_utils import insert_record
from download_utils import download_zip_file, download_file
from date_utils import format_date
import logging

logger = logging.getLogger(__name__)


def fetch_technical_from_ichart(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    file_name = 'ichart_' + format_date(date) + '.csv'
    download_url = 'https://www.icharts.in/includes/screener/EODScan.php?export=1'
    logger.info(f"downloading delivery data from {download_url}")
    download_file(download_url, dir, file_name)
    #store_delivery_data(dir, file_name, date)


def store_delivery_data(dir, file_name, date):
    logger.debug("Storing the raw delivery data in DB from {file_name}")
