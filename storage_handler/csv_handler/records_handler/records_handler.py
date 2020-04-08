import configparser
import datetime
import logging
import re
import preprocessor as prep
import html
import constants as const


class RecordsHandler(object):
    """Handles collection of tweets as records for the CSV file.
    Methods deal with processing and formatting tweet attributes before they
    are stored in the .csv file columns. The list of the .csv columns is
    defined in the attribute `interesting_attributes`.

    Attributes:
    -----------
    - `tweets_handler`: a an handler for tweet objects
    - `clean_flag`: boolean flag, if True it will add a column `cleaned_text`
      to them .csv file. `cleaned_text` column represents `full_text` without
      urls, hashtags or usernames.
    - `interesting_attributes`: list of strings representing the tweets attributes
      to save in the .csv. The list is read from `ATTR_FILE_INI`.

    Methods:
    --------
    - `get_only_interesting_attributes(self)`: returns a list of dictionaries
      representing the tweets; only the tweet attributes defined in `interesting_attributes`
      are stored in the dictionaries.
    """


    def __init__(self, tweets_handler, args):
        """Initializes RecordsHandler

        Parameters:
        -----------
        - `tweets_handler`: an object wrapping a list of tweet
        - `args`: argparse data structure; it must contains:
            - `clean`: boolean flag, if True it will add a column `cleaned_text`
                        to them .csv file. `cleaned_text` column represents
                        `full_text` without urls, hashtags or usernames."""
        self.tweets_handler = tweets_handler
        self.clean_flag = args.clean
        self.interesting_attributes = self._get_list_of_interesting_attributes()

    def _get_list_of_interesting_attributes(self):
        interesting_attributes = self._extract_interesting_attributes_from_config()
        interesting_attributes = self._handle_specific_case(interesting_attributes)
        return interesting_attributes

    def _extract_interesting_attributes_from_config(self):
        config = configparser.ConfigParser()
        config.read(const.ATTR_FILE_INI)
        config_attributes = config['interesting-attributes']['attrs']
        interesting_attributes = config_attributes.split(',')
        return interesting_attributes

    def _handle_specific_case(self, interesting_attributes):
        if self.clean_flag:
            interesting_attributes.append('cleaned_text')
        return interesting_attributes

    def get_only_interesting_attributes(self):
        """Isolates just the interesting attributes of the tweets.
        Interesting attributes are defined in `ATTR_FILE_INI`.
        """
        logging.debug('Getting attributes: {}'
                     .format(self.interesting_attributes))
        formatted_tweets = self.tweets_handler.format_attributes(self.interesting_attributes)
        records = [{key: getattr(tweet, key)
                    for key in self.interesting_attributes}
                   for tweet in formatted_tweets]
        return records
