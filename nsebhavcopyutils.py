import csv
from mongoutils import insertrecord
from downloadutils import downloadzipfile

monthtext = {'01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR', '05': 'MAY', '06': 'JUN',
             '07': 'JUL', '08': 'AUG', '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'}


def getnsebhavcopy(date, dir):
    day, month, year = '%02d' % date.day, '%02d' % date.month, '%02d' % date.year
    filename = 'cm'+day+monthtext[month]+year+'bhav.csv'
    nsebhavzipurl = 'https://www1.nseindia.com/content/historical/EQUITIES/' + \
        year+'/' + monthtext[month]+'/' + filename+'.zip'
    #downloadzipfile(nsebhavzipurl, dir)
    storebhavcopy(dir, filename)


def storebhavcopy(dir, filename):
    print('Getting CSV: ' + dir + filename)
    file = open(dir+filename, 'r')
    csv_file = csv.DictReader(file)
    for row in csv_file:
        rowdict = dict(row)
        rowdict["_id"] = rowdict["ISIN"] + "_" + rowdict["TIMESTAMP"]
        del rowdict['']
        insertrecord("nse_bhav_raw", rowdict)
