import time
import datetime
import logging
import csv
import os
import pandas as pd
import constants as const
from records_handler import RecordsHandler


class CSVFileHandler(object):
    """Handles the creation of the CSV file.
    The main method is `export_csv()` which exports .csv file containing the
    retrieved tweets. It uses `pandas` python module to deal with the creation
    of the .csv file. The name of the file depends on the chosen search type:
    - if `by-keyword` the filename will be something like `tweets_with_`;
    - if `by-user` the filename will be something like `tweets_by_`;
    - if `by-keywords-list` or `by-users-list` the filename will be something
      like `tweets_from_`.

    Attributes:
    -----------
    - `query_word`: word or username to be searched.
    - `search_type`: type of search (by user or by keyword).
    - `out_dir`: directory in which the .csv file will be created.
    - `append_to`: boolean flag, if True new tweets will be stored in the most
                 recent .csv file. If False, a new .csv file will be created.
    - `clean`: boolean flag, if True it will add a column `cleaned_text` to them
             .csv file. `cleaned_text` column represents `full_text` without
             urls, hashtags or usernames.
    - `recordsHandler`: a RecordsHandler object; it deals with the preprocessing
      and formatting of the tweet attributes.
    - `records`: a list of dictionaries representing the tweets.

    Methods:
    --------
    - `name_csv_file(self)`: returns a string representing the .csv file name.
    - `name_csv_file_with_timestamp(self)`: returns a string representing the .csv
      file name with a timestamp.
    - `get_list_of_csv_file_in_out_dir_with_prefix(self, prefix)`: returns a list
      of .csv filenames in `out_dir` starting with the given `prefix`.
    - `export_csv(self)`: creates the .csv file containing the retrieved tweets.
    """


    def __init__(self, query_word, search_type, out_dir, append_to, clean, tweets):
        """Initializes CSVFileHandler

        Parameters:
        -----------
        - `query_word`: word or username to be searched
        - `search_type`: type of search (by user or by keyword)
        - `out_dir`: directory in which the .csv file will be created
        - `append_to`: boolean flag, if True new tweets will be stored in the most
                     recent .csv file. If False, a new .csv file will be created.
        - `clean`: boolean flag, if True it will add a column `cleaned_text` to them
                 .csv file. `cleaned_text` column represents `full_text` without
                 urls, hashtags or usernames.
        - `tweets`: a list of `Status` object from `python-twitter` module,
          each representing a single tweet."""
        self.query_word = query_word.replace(' ', '_')
        self.search_type = search_type
        self.out_dir = out_dir
        self.append_to = append_to
        self.records_handler = RecordsHandler(tweets, clean)
        self.records = self.records_handler.get_only_interesting_attributes()


    def name_csv_file(self):
        """Names the CSV file based on query. No file extension."""
        preposition = 'with'
        if self.search_type not in ['by-keywords-list', 'by-users-list']:
            if self.search_type == 'by-user':
                preposition = 'by'
            return '_'.join(['tweets', preposition, self.query_word])
        else:
            preposition = 'from'
            filename_without_extension = self.query_word.split('.')[0]
            return '_'.join(['tweets', preposition, filename_without_extension])


    def name_csv_file_with_timestamp(self):
        """Names the CSV file based on timestamp and query. No file extension."""
        timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
        header = self.name_csv_file()
        filename = '_'.join([header, timestamp])
        return '/'.join([self.out_dir, filename])


    def get_list_of_csv_file_in_out_dir_with_prefix(self, prefix):
        """Returns a list of CSV file starting with the substring 'prefix'"""
        files = os.listdir(self.out_dir)
        files.sort()
        files.reverse()
        return [f for f in files if f.startswith(prefix) and f.endswith('.csv')]


    def export_csv(self):
        """Exports CSV file."""
        logging.debug('Exporting file \'{}\'...'.format(self.name_csv_file()))
        dataframe = pd.DataFrame(self.records)
        if dataframe.shape[0] > 0:
            filename = '{}.csv'.format(self.name_csv_file_with_timestamp())
            if self.append_to == True:
                prefix = self.name_csv_file()
                csv_files = self.get_list_of_csv_file_in_out_dir_with_prefix(prefix)
                if len(csv_files) > 0:
                    filename = csv_files[0]
                    logging.debug('Appending to CSV file \'{}\'...'.format(filename))
                    existing_dataframe = pd.read_csv(filename,
                                                     sep=const.CSV_SEPARATOR)
                    dataframe = dataframe.append(existing_dataframe)
                    dataframe.drop_duplicates(inplace=True, subset=['created_at', 'user'])
                else:
                    logging.debug('No previous CSV file found')
            dataframe.sort_values(const.CSV_SORTED_BY, inplace=True)
            dataframe.to_csv(filename,
                             index=False,
                             quotechar='"',
                             quoting=csv.QUOTE_NONNUMERIC,
                             encoding=const.CSV_ENCODING,
                             escapechar='\\',
                             sep=const.CSV_SEPARATOR)
            if self.append_to == True:
                logging.info('Appended tweets to CSV file \'{}\''.format(filename))
            else:
                logging.info('Created CSV file \'{}\''.format(filename))
        else:
            logging.info('No tweets retrieved for keyword \'{}\''
                         .format(self.query_word))
