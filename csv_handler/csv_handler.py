import time
import datetime
import logging
import csv
import pandas as pd
import constants as const
from records_handler import RecordsHandler


class CSVFileHandler(object):
    """Handles the creation of the CSV file."""


    def __init__(self, args, tweets):
        self.query_word = args.query_word.replace(' ', '_')
        self.search_type = args.search_type
        self.out_dir = args.out_dir
        self.records_handler = RecordsHandler(tweets)
        self.records = self.records_handler.get_only_interesting_attributes()


    def name_csv_file(self):
        """Names the CSV file based on timestamp and query."""
        timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        timestamp = ''.join([timestamp, '.csv'])
        preposition = 'with'
        if self.search_type == 'by-user':
            preposition = 'from'
        header = '_'.join(['tweets', preposition, self.query_word])
        filename = '_'.join([header, timestamp])
        return '/'.join([self.out_dir, filename])


    def export_csv(self):
        """Exports CSV file."""
        logging.debug('Exporting file \'{}\'...'.format(self.name_csv_file()))
        dataframe = pd.DataFrame(self.records)
        if dataframe.shape[0] > 0:
            dataframe.sort_values(const.CSV_SORTED_BY, inplace=True)
            dataframe.to_csv(self.name_csv_file(), index=False,
                             quoting=csv.QUOTE_NONE,
                             encoding=const.CSV_ENCODING,
                             escapechar='\\')
            logging.info('Created file \'{}\''.format(self.name_csv_file()))
        else:
            logging.info('No tweets retrieved for keyword \'{}\''
                         .format(self.query_word))
