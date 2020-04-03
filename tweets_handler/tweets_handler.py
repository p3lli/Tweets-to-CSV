import logging
import configparser
import twitter
import constants as const
import os.path


class ApiHandler(object):
    """Class that handles all the Twitter API comunication.
    It uses `python-twitter` module to retrieve tweets by user or by keyword.
    API keys must be stored in `CRED_FILE_INI` file.
    The main method is `get_tweets(self)` which calls `GetSearch` or
    `GetUserTimeline` methods from `python-twitter` module to retrieve tweets
    based on the `search_type` value.

    Attributes:
    -----------
    - `query_word`: word or username to be searched. It can also be the name of
      the file containing the list of keywords or usernames to be searched.
    - `search_type`: type of search (`by-user`, `by-keyword`, `by-users-list`,
      `by-keywords-list`).
    - `api`: `twitter.API` wrapper object which deals with the communication to
      the Twitter API.

    Methods:
    --------
    - `get_tweets(self)`: gets tweets based on keyword or username.
    - `get_tweets_by_keyword(self)`: gets tweets based on keyword.
    - `get_tweets_by_user(self)`: gets tweets based on user name.
    - `get_tweets_by_list_of_keywords(self)`: gets tweets based on a list of keywords.
    - `get_tweets_by_list_of_users(self)`: gets tweets based on a list of users.
    - `read_list_from_file(self)`: reads list of keyword or users from a text file."""


    def __init__(self, args):
        """Initializes ApiHandler

        Parameters:
        -----------
        - `args`: argparse data structure; it must contains:
            - `query_word`: word or username to be searched
            - `search_type`: type of search (by user or by keyword)
            - `ntweets`: maximum number of tweets to be retrieved"""
        if args:
            self.query_word = args.query_word
            self.search_type = args.search_type
            self.number_of_tweets = self._set_number_of_tweets(args.ntweets)
            self.api = self._get_credentials()


    def _set_number_of_tweets(self, ntweets):
            if ntweets:
                return ntweets
            else:
                return const.MAX_NUMBER_OF_TWEETS


    def _get_credentials(self):
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


    def get_tweets(self):
        """Gets tweets based on keywords or username. Returns a list of
        `tweet.Status` object representing the retrieved tweets."""
        return eval(const.GET_TWEETS_BY[self.search_type])


    def get_tweets_by_keyword(self):
        """Gets tweets based on keyword."""
        logging.debug('Getting tweets with keyword(s): {}'
                .format(self.query_word))
        try:
            results = self._retrieve_tweets_by_term(self.query_word)
        except Exception, e:
            logging.warning('A problem occurred for keyword "{}": {}'
                    .format(self.query_word, str(e)))
        return results


    def get_tweets_by_user(self):
        """Gets tweets based on user name."""
        logging.debug('Getting tweets from user: {}'
                .format(self.query_word))
        try:
            results = self._retrieve_tweets_by_screen_name(self.query_word)
        except Exception, e:
            logging.warning('A problem occurred for screen name "{}": {}'
                    .format(self.query_word, str(e)))
        return results


    def get_tweets_by_list_of_keywords(self):
        """Gets tweets based on list of keywords."""
        logging.debug('Getting tweets with keywords from file: {}'
                .format(self.query_word))
        query_words = self.read_list_from_file()
        list_results = []
        for query_word in query_words:
            try:
                results = self._retrieve_tweets_by_term(query_word)
                list_results.extend(results)
            except Exception, e:
                logging.warning('A problem occurred for keyword "{}": {}'
                        .format(query_word, str(e)))
        return list_results


    def get_tweets_by_list_of_users(self):
        """Gets tweets based on list of users."""
        logging.debug('Getting tweets by users from file: {}'
                .format(self.query_word))
        query_words = self.read_list_from_file()
        list_results = []
        for query_word in query_words:
            try:
                results = self._retrieve_tweets_by_screen_name(query_word)
                list_results.extend(results)
            except Exception, e:
                logging.warning('A problem occurred for screen name "{}": {}'
                        .format(query_word, str(e)))
        return list_results


    def _retrieve_tweets_by_term(self, query_word):
        return self.api.GetSearch(term=query_word,
                                 count=self.number_of_tweets,
                                 include_entities=const.INCLUDE_ENTITIES)


    def _retrieve_tweets_by_screen_name(self, screen_name):
        return self.api.GetUserTimeline(screen_name=screen_name,
                                       count=self.number_of_tweets,
                                       exclude_replies=const.EXCLUDE_REPLIES)


    def read_list_from_file(self):
        """Reads list of keyword or users from a text file."""
        query_words = []
        if os.path.isfile(self.query_word):
            logging.info('Reading query words from {}'.format(self.query_word))
            query_words = [line.rstrip('\n') for line in open(self.query_word) if line != '\n']
            logging.debug('Query words are: {}'.format(', '.join(query_words)))
        else:
            logging.warn('{} is not a file'.format(self.query_word))
        return query_words
