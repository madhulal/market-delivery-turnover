from mongo_utils import insert_record, get_records, get_db, get_record, drop_collection
from date_utils import format_date, format_date_string
from datetime import date
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def combine_bse_and_nse_datas(date):
    # Get all rows for given
    formatted_date = format_date(date)
    cursor = get_records(
        'nse_combined', {'date': formatted_date})
    for nse_combined_record in cursor:
        isin = nse_combined_record['isin']
        nse_symbol = nse_combined_record['symbol']
        series = nse_combined_record['series']
        # Get BSE combined record
        bse_combined_record = get_record(
            'bse_combined', {'date': formatted_date, 'isin': isin})
        if bse_combined_record is None:
            logger.warning('Unable to find the BSE record for NSE symbol: {} under series: {} and isin: {} for date: {}'.format(
                nse_symbol, series, isin, formatted_date))
        else:
            try:
                id = nse_combined_record['_id']
                date = formatted_date
                bse_symbol = bse_combined_record['symbol']
                nse_turnover = nse_combined_record['turnover']
                bse_turnover = bse_combined_record['turnover']
                total_turnover = float(nse_turnover) + float(bse_turnover)
                nse_delivery_turnover = nse_combined_record['delivery_turnover']
                bse_delivery_turnover = bse_combined_record['delivery_turnover']
                total_delivery_turnover = float(
                    nse_delivery_turnover) + float(bse_delivery_turnover)
                delivery_percentage = total_delivery_turnover * 100 / total_turnover

                bse_nse_combined_dict = {}
                bse_nse_combined_dict['_id'] = id
                bse_nse_combined_dict['date'] = date
                bse_nse_combined_dict['bse_symbol'] = bse_symbol
                bse_nse_combined_dict['nse_symbol'] = nse_symbol
                bse_nse_combined_dict['series'] = series
                bse_nse_combined_dict['close_price'] = nse_combined_record["close_price"]
                bse_nse_combined_dict['turnover'] = total_turnover
                bse_nse_combined_dict['delivery_turnover'] = total_delivery_turnover
                bse_nse_combined_dict['delivery_percentage'] = delivery_percentage

                insert_record("bse_nse_combined", bse_nse_combined_dict)
            except Exception as e:
                logger.error(
                    'Failed to process data for NSE record {} and BSE record {} with exception {}'
                    .format(nse_combined_record, bse_combined_record, e))


drop_collection("bse_nse_combined")
request_date = date(2020, 7, 23)
combine_bse_and_nse_datas(request_date)
