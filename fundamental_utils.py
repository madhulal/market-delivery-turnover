from mongo_utils import insert_record, update_record
from date_utils import format_date, format_date_string
import logging
import pandas as pd
import csv
from json_utils import write_dict_to_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def fetch_fundamentals(dir, file_name, date):
    # Convert xlsx to csv
    read_file = pd.read_excel(dir + file_name)
    write_file = dir + file_name + '_' + format_date(date) + '.csv'
    read_file.to_csv(write_file, index=None, header=True)
    store_data(dir, write_file)


def store_data(dir, file):
    logger.debug("Storing the fundamental data in DB from {file}")
    csv_file = open(file, 'r')
    csv_file_dic = csv.DictReader(csv_file)
    for row in csv_file_dic:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["SecID"]
        logger.debug(rowdict)
        #update_record("fundamental", rowdict)
        write_dict_to_file(rowdict, dir + 'test.json')
    logger.info('Fundamental data is pushed to DB')
