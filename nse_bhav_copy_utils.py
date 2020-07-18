import csv
from mongo_utils import insert_record
from download_utils import download_zip_file, download_file
from date_utils import format_date

monthtext = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN',
             '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}


def get_nse_delivery_data(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    file_name = 'MTO_'+ day + month + year +'.DAT'
    download_url = 'https://www1.nseindia.com/archives/equities/mto/' + file_name
    print(download_url)
    download_file(download_url, dir, file_name)
    #store_delivery_data(dir, file_name)

def get_nse_bhav_copy(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    filename = 'cm'+day+monthtext[month]+year+'bhav.csv'
    nsebhavzipurl = 'https://www1.nseindia.com/content/historical/EQUITIES/' + \
        year+'/' + monthtext[month]+'/' + filename+'.zip'
    download_zip_file(nsebhavzipurl, dir)
    store_bhav_copy(dir, filename)


def store_bhav_copy(dir, filename):
    print('Getting CSV: ' + dir + filename)
    file = open(dir+filename, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["ISIN"] + "_" + \
            format_date(rowdict["TIMESTAMP"], '%d-%b-%Y')
        del rowdict['']
        # print(rowdict)
        insert_record("nse_bhav_raw", rowdict)
