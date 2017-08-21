import logging
import configparser
import twitter
import constants as const


class ApiHandler(object):
    """Class that handles all the Twitter API comunication."""


    def __init__(self, query_word, search_type):
        self.query_word = query_word
        self.search_type = search_type
        self.api = self.get_credentials()


    def get_credentials(self):
        """Get credentials from CRED_FILE_INI."""
        config = configparser.ConfigParser()
        config.read(const.CRED_FILE_INI)
        credentials = config['twitter-api']
        api = twitter.Api(consumer_key=credentials['consumer_key'],
                consumer_secret=credentials['consumer_secret'],
                access_token_key=credentials['access_token_key'],
                access_token_secret=credentials['access_token_secret'])
        return api


    def get_tweets_by_keyword(self):
        """Gets tweets based on keyword."""
        logging.debug('Getting tweets with keyword(s): {}'
                .format(self.query_word))
        results = self.api.GetSearch(term=self.query_word,
                                     count=const.MAX_COUNT_KEYWORD,
                                     include_entities=const.INCLUDE_ENTITIES)
        return results


    def get_tweets_by_user(self):
        """Gets tweets based on user name."""
        logging.debug('Getting tweets from user: {}'
                .format(self.query_word))
        results = self.api.GetUserTimeline(screen_name=self.query_word,
                                           count=const.MAX_COUNT_USER,
                                           exclude_replies=const.EXCLUDE_REPLIES)
        return results


    def get_tweets(self):
        """Gets tweets based on keywords or username."""
        return eval(const.GET_TWEETS_BY[self.search_type])
