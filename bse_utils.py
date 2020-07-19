import csv
from download_utils import download_zip_file_mozilla_agent
from date_utils import format_date
from mongo_utils import insert_record


def get_bse_bhav_copy(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % (
        abs(date.year) % 100)
    filename = 'EQ_ISINCODE_' + day + month + year+'.zip'
    bhavurl = 'https://www.bseindia.com/download/BhavCopy/Equity/' + filename
    #download_zip_file_mozilla_agent(bhavurl, dir)
    updated_file_name = filename.replace("zip", "CSV")
    store_bhav_copy(dir, updated_file_name)


def store_bhav_copy(dir, file):
    print('Getting CSV: ' + dir + file)
    file = open(dir+file, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["ISIN_CODE"] + \
            "_" + format_date_string(rowdict["TRADING_DATE"], '%d-%b-%y')
        # print(rowdict)
        insert_record("bse_bhav_raw", rowdict)
