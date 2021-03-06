import logging
import os.path
import constants as const
from tweets_handler import TweetsHanlder
from twitter_api_wrapper import TwitterApiHandler


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
            self.api = TwitterApiHandler(args.ntweets)


    def get_tweets(self):
        """Gets tweets based on keywords or username. Returns a list of
        `tweet.Status` object representing the retrieved tweets."""
        results = eval(const.GET_TWEETS_BY[self.search_type])
        tweets = TweetsHanlder.create_tweets_handler(results)
        return tweets


    def get_tweets_by_keyword(self):
        """Gets tweets based on keyword."""
        logging.debug('Getting tweets with keyword(s): {}'
                .format(self.query_word))
        retults = []
        try:
            results = self.api.retrieve_tweets_by_term(self.query_word)
        except Exception, e:
            logging.warning('A problem occurred for keyword "{}": {}'
                    .format(self.query_word, str(e)))
        return results


    def get_tweets_by_user(self):
        """Gets tweets based on user name."""
        logging.debug('Getting tweets from user: {}'
                .format(self.query_word))
        results = []
        try:
            results = self.api.retrieve_tweets_by_screen_name(self.query_word)
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
                results = self.api.retrieve_tweets_by_term(query_word)
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
                results = self.api.retrieve_tweets_by_screen_name(query_word)
                list_results.extend(results)
            except Exception, e:
                logging.warning('A problem occurred for screen name "{}": {}'
                        .format(query_word, str(e)))
        return list_results


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
