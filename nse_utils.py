import csv
from mongo_utils import insert_record
from download_utils import download_zip_file, download_file
from date_utils import format_date, format_date_string
import logging
import subprocess


monthtext = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN',
             '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        rowdict["_id"] = rowdict["ISIN"] + "_" + \
            format_date_string(rowdict["TIMESTAMP"], '%d-%b-%Y')
        del rowdict['']
        logger.debug('Inserting NSE bhav copy data {rowdict} to DB')
        insert_record("nse_bhav_raw", rowdict)
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

    # The file needs to be excluded first three lines alsomissed the series
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
        rowdict["_id"] = rowdict["Name of Security"] + "_" + \
            rowdict["Series"] + "_" + \
            format_date(date)
        del rowdict['Record Type']
        del rowdict['Sr No']
        logger.debug('Inserting NSE delivery data {} to DB'.format(rowdict))
        insert_record("nse_delivery_raw", rowdict)
    logger.info('NSE delivery data is pushed to DB')
