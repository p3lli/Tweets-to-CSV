import configparser
import twitter
import constants as const
from tweets_handler import MockTweet


class TwitterApiHandler(object):
    """Factory class for twitter api handlers.
    It reads `TWITTER_API` from constants and then create its own api handler.
    It exposes the methods `retrieve_tweets_by_term()` and
    `retrieve_tweets_by_screen_name()`.

    Attributes:
    -----------
    - `api_handler`: wrapper for a specific Twitter API
    """

    def __init__(self, max_number_of_tweets, api_handler_type, test_tweets):
        """Initializes TwitterApiHandler

        Parameters
        ----------
        - `max_number_of_tweets`: max number of tweets asked
        - `api_handler_type`: API handler type
        """
        if api_handler_type == 'python-twitter':
            self.api_handler = PythonTwitterApiHandler(max_number_of_tweets)
        elif api_handler_type == 'mock':
            self.api_handler = MockApiHandler(max_number_of_tweets, test_tweets)
        else:
            raise ValueError(api_handler_type)

    def retrieve_tweets_by_term(self, query_word):
        """Wrapper method to `retrieve_tweets_by_term()` method of
        the concrete wrapper object"""
        return self.api_handler.retrieve_tweets_by_term(query_word)

    def retrieve_tweets_by_screen_name(self, screen_name):
        """Wrapper method to `retrieve_tweets_by_screen_name()` method
        of the concrete wrapper object"""
        return self.api_handler.retrieve_tweets_by_screen_name(screen_name)


class PythonTwitterApiHandler(object):
    """Api handler concrete implementation for module python-twitter
    https://github.com/bear/python-twitter
    """

    def __init__(self, max_number_of_tweets):
        self.api = self._initialize_api_client()
        self.max_number_of_tweets = self._set_number_of_tweets(max_number_of_tweets)


    def retrieve_tweets_by_term(self, query_word):
        return self.api.GetSearch(term=query_word,
                                 count=self.max_number_of_tweets,
                                 include_entities=const.INCLUDE_ENTITIES)


    def retrieve_tweets_by_screen_name(self, screen_name):
        return self.api.GetUserTimeline(screen_name=screen_name,
                                       count=self.max_number_of_tweets,
                                       exclude_replies=const.EXCLUDE_REPLIES)


    def _initialize_api_client(self):
        """Gets credentials from `CRED_FILE_INI`. Returns a `twitter.API` wrapper
        object which deals with the communication to the Twitter API."""
        credentials = self._read_credentials_from_config_file()
        api = twitter.Api(consumer_key=credentials['consumer_key'],
                consumer_secret=credentials['consumer_secret'],
                access_token_key=credentials['access_token_key'],
                access_token_secret=credentials['access_token_secret'],
                tweet_mode='extended',
                input_encoding='utf8')
        return api


    def _read_credentials_from_config_file(self):
        config = configparser.ConfigParser()
        config.read(const.CRED_FILE_INI)
        return config['twitter-api']


    def _set_number_of_tweets(self, ntweets):
            if ntweets:
                return ntweets
            else:
                return const.MAX_NUMBER_OF_TWEETS

class MockApiHandler(object):

    def __init__(self, max_number_of_tweets, test_tweets):
        self.max_number_of_tweets = max_number_of_tweets
        self.tweets = test_tweets

    def retrieve_tweets_by_term(self, query_word):
        results = []
        for tweet in self.tweets:
            if tweet['full_text'] and query_word in tweet['full_text']:
                results.append(tweet)
                if len(results) == self.max_number_of_tweets:
                    break
        return results

    def retrieve_tweets_by_screen_name(self, query_word):
        results = []
        for tweet in self.tweets:
            if tweet['user'] and query_word == tweet['user']:
                results.append(tweet)
                if len(results) == self.max_number_of_tweets:
                    break
        return results
