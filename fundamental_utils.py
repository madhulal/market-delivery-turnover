from mongo_utils import insert_record, get_db, get_record_by_id
from date_utils import format_date, format_date_string
import logging
import pandas as pd
import csv
from json_utils import write_dict_to_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def update_header(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        f.close

    lines[0] = lines[0].replace('.', '')

    new_file = open(file_path, 'w')
    new_file.writelines(lines)
    new_file.close


def fetch_fundamentals(dir, file_name, date):
    # Convert xlsx to csv
    read_file = pd.read_excel(dir + file_name)
    write_file = dir + file_name + '_' + format_date(date) + '.csv'
    read_file.to_csv(write_file, index=None, header=True)
    update_header(write_file)
    store_data(dir, write_file)


def store_data(dir, file):
    logger.debug("Storing the fundamental data in DB from {}".format(file))
    csv_file = open(file, 'r')
    csv_file_dic = csv.DictReader(csv_file)
    for row in csv_file_dic:
        rowdict = dict(row)
        id = rowdict["SecID"]
        rowdict["_id"] = id
        logger.debug(rowdict)

        existing_record = get_record_by_id("fundamental", id)
        if existing_record is None:
            logger.debug(
                'Inserting fundamental data {} to DB'.format(rowdict))
            insert_record("fundamental", rowdict)
        else:
            logger.debug(
                'Updating fundamental data {} to DB'.format(rowdict))
            get_db().fundamental.update_one(
                {'_id': id}, {"$set": rowdict}, upsert=False)

        #write_dict_to_file(rowdict, dir + 'test.json')
    logger.info('Fundamental data is pushed to DB')
