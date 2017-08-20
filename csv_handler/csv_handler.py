import pandas as pd
import configparser

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


    def get_only_interesting_attributes(self):
        """Isolates just the interesting attributes of the tweets."""
        if 'user' in self.interesting_attributes:
            self.extract_user_name()
        records = [{key: getattr(tweet, key)
                    for key in self.interesting_attributes}
                   for tweet in self.tweets]
        return records
