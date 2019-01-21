import logging
import configparser
import twitter
import constants as const
import os.path


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
                access_token_secret=credentials['access_token_secret'],
                tweet_mode='extended')
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


    def get_tweets_by_list_of_keywords(self):
        """Gets tweets based on list of keywords."""
        logging.debug('Getting tweets with keywords from file: {}'
                .format(self.query_word))
        query_words = self.read_list_from_file()
        list_results = []
        for query_word in query_words:
            results = self.api.GetSearch(term=query_word,
                                         count=const.MAX_COUNT_KEYWORD,
                                         include_entities=const.INCLUDE_ENTITIES)
            list_results.extend(results)
        return list_results


    def get_tweets_by_list_of_users(self):
        """Gets tweets based on list of users."""
        logging.debug('Getting tweets by users from file: {}'
                .format(self.query_word))
        query_words = self.read_list_from_file()
        list_results = []
        for query_word in query_words:
            results = self.api.GetUserTimeline(screen_name=query_word,
                                               count=const.MAX_COUNT_USER,
                                               exclude_replies=const.EXCLUDE_REPLIES)
            list_results.extend(results)
        return list_results


    def read_list_from_file(self):
        query_words = []
        if os.path.isfile(self.query_word):
            logging.info('Reading query words from {}'.format(self.query_word))
            query_words = [line.rstrip('\n') for line in open(self.query_word)]
            logging.debug('Query words are: {}'.format(', '.join(query_words)))
        else:
            logging.warn('{} is not a file'.format(self.query_word))
        return query_words


    def get_tweets(self):
        """Gets tweets based on keywords or username."""
        return eval(const.GET_TWEETS_BY[self.search_type])
