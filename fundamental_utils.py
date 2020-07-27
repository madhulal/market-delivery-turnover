from mongo_utils import insert_record, get_db, get_record_by_id, drop_collection
from date_utils import format_date, format_date_string
import logging
import pandas as pd
import csv
from json_utils import write_dict_to_file
from datetime import date
from config import is_fundamnetal_enabled
from settings import DATA_FOLDER, FUNDAMENTALS_FILE_NAME

logger = logging.getLogger(__name__)


def drop_collections():
    logger.warning('Clearing fundamental collections')
    drop_collection("fundamental")


def update_header(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        f.close

    lines[0] = lines[0].replace('.', '')

    new_file = open(file_path, 'w')
    new_file.writelines(lines)
    new_file.close


def fetch_fundamentals(date):
    # drop_collections()
    if(is_fundamnetal_enabled()):
        # Convert xlsx to csv
        read_file = pd.read_excel(DATA_FOLDER + FUNDAMENTALS_FILE_NAME)
        write_file = dir + file_name + '_' + format_date(date) + '.csv'
        read_file.to_csv(write_file, index=None, header=True)
        update_header(write_file)
        store_data(dir, write_file)
    else:
        logger.warning('Fundamental not enabled')


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


def test():
    request_date = date(2020, 7, 9)
    # drop_collections()
    fetch_fundamentals(request_date)


# test()
