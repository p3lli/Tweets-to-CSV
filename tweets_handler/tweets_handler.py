import twitter
import logging
import configparser

CRED_FILE_INI = './tweets_handler/resources/twitter_api_credentials.ini'
HASHTAG_SYMBOL = '%23'

class ApiHandler(object):
    """Class that handles all the Twitter API comunication."""

    def __init__(self, query_word):
        self.query_word = query_word
        self.api = self.get_credentials()
    

    def get_credentials(self):
        """Get credentials from CRED_FILE_INI"""
        config = configparser.ConfigParser()
        config.read(CRED_FILE_INI)
        print config.sections()
        credentials = config['twitter-api']
        api = twitter.Api(consumer_key=credentials['consumer_key'],
                consumer_secret=credentials['consumer_secret'],
                access_token_key=credentials['access_token_key'],
                access_token_secret=credentials['access_token_secret'])
        return api


    def get_tweets(self):
        """Gets tweets containing a specific hashtag"""
        logging.debug("Getting tweets with hashtag: #{}"
                .format(self.query_word))
        raw_query = 'q=' + HASHTAG_SYMBOL + self.query_word
        results = self.api.GetSearch(raw_query=raw_query)
        return results


