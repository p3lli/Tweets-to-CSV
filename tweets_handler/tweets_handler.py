import twitter
import logging
import configparser


class ApiHandler(object):
    """Class that handles all the Twitter API comunication."""
    CRED_FILE_INI = './tweets_handler/resources/twitter_api_credentials.ini'
    HASHTAG_SYMBOL = '%23'
    MAX_COUNT_KEYWORD = 100
    MAX_COUNT_USER = 200
    INCLUDE_ENTITIES = True
    EXCLUDE_REPLIES = False
    GET_TWEETS_BY = {'by-keyword': 'self.get_tweets_by_keyword()',
                     'by-user': 'self.get_tweets_by_user()'}

    def __init__(self, query_word, search_type):
        self.query_word = query_word
        self.search_type = search_type
        self.api = self.get_credentials()


    def get_credentials(self):
        """Get credentials from CRED_FILE_INI"""
        config = configparser.ConfigParser()
        config.read(self.CRED_FILE_INI)
        credentials = config['twitter-api']
        api = twitter.Api(consumer_key=credentials['consumer_key'],
                consumer_secret=credentials['consumer_secret'],
                access_token_key=credentials['access_token_key'],
                access_token_secret=credentials['access_token_secret'])
        return api


    def get_tweets_by_keyword(self):
        """Gets tweets based on keyword"""
        logging.debug("Getting tweets with keyword(s): {}"
                .format(self.query_word))
        results = self.api.GetSearch(term=self.query_word,
                                     count=self.MAX_COUNT_KEYWORD,
                                     include_entities=self.INCLUDE_ENTITIES)
        return list(set([status.text for status in results]))


    def get_tweets_by_user(self):
        """Gets tweets based on user name"""
        logging.debug("Getting tweets from user: {}"
                .format(self.query_word))
        results = self.api.GetUserTimeline(screen_name=self.query_word,
                                           count=self.MAX_COUNT_USER,
                                           exclude_replies=self.EXCLUDE_REPLIES)
        return [status.text for status in results]


    def get_tweets(self):
        """Gets tweets based on keywords or username"""
        return eval(self.GET_TWEETS_BY[self.search_type])
