import pandas as pd
import logging
import configparser
import datetime
import csv
import time


class RecordsHandler(object):
    """Handles collection of tweets."""
    ATTR_FILE_INI = './csv_handler/resources/interesting_attributes.ini'

    def __init__(self, tweets):
        self.tweets = tweets
        config = configparser.ConfigParser()
        config.read(self.ATTR_FILE_INI)
        config_attributes = config['interesting-attributes']['attrs']
        self.interesting_attributes = config_attributes.split(',')


    def extract_user_name(self):
        """Extracts the screen name from the object User."""
        for tweet in self.tweets:
            tweet.user = tweet.user.screen_name


    def convert_timestamp_created_at(self):
        """Converts 'created_at' attribute in timestamp."""
        created_at_old_format = '%a %b %d %H:%M:%S +0000 %Y'
        created_at_new_format = '%Y-%m-%d %H:%M:%S'
        for tweet in self.tweets:
            tuple_timestamp = time.strptime(tweet.created_at,
                                            created_at_old_format)
            tweet.created_at = time.strftime(created_at_new_format,
                                             tuple_timestamp)


    def format_text(self):
        """Formats 'text' attribute."""
        for tweet in self.tweets:
            tweet.text = tweet.text.replace('\n', ' ')
            tweet.text = tweet.text.replace(',', '')


    def get_only_interesting_attributes(self):
        """Isolates just the interesting attributes of the tweets."""
        if 'user' in self.interesting_attributes:
            self.extract_user_name()
        if 'created_at' in self.interesting_attributes:
            self.convert_timestamp_created_at()
        if 'text' in self.interesting_attributes:
            self.format_text()
        logging.debug('Getting attributes: {}'
                     .format(self.interesting_attributes))
        records = [{key: getattr(tweet, key)
                    for key in self.interesting_attributes}
                   for tweet in self.tweets]
        return records


class CSVFileHandler(object):
    """Handles the creation of the CSV file."""

    def __init__(self, args, records):
        self.query_word = args.query_word.replace(' ', '_')
        self.search_type = args.search_type
        self.out_dir = args.out_dir
        self.records = records


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
        dataframe.sort_values('created_at', inplace=True)
        dataframe.to_csv(self.name_csv_file(), index=False,
                         quoting=csv.QUOTE_NONE, encoding='utf-8',
                         escapechar='\\')
        logging.info('Created file \'{}\''.format(self.name_csv_file()))
