import csv
from mongo_utils import get_records
import logging
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt


def get_data(symbol):
    cursor = get_records(
        'nse_combined', {'symbol': symbol, 'series': 'EQ'}, {'_id': 0, 'date': 1, 'close_price': 1, 'volume': 1})
    output = []
    for nse_combined_record in cursor:
        graph_data = {}
        date = nse_combined_record['date']
        price = float(nse_combined_record['close_price'])
        graph_data["date"] = date
        graph_data['price'] = price
        output.append(graph_data)
    scores_data = pd.DataFrame(output, index=None)
    scores_data.plot(x='date', y='price', kind='line')
    plt.show()


get_data('ASIANPAINT')
