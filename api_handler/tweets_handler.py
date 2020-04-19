import datetime
import logging
import preprocessor as prep
import re
import time
import constants as const

class TweetsHanlder(object):
    """Factory class for tweets handlers.
    It reads `TWITTER_API` from constants and then create its own api handler.
    """

    @staticmethod
    def create_tweets_handler(tweets):
        """Create a Tweets Hanlder and returns it

        Parameters
        ----------
        - `tweets`: retrieved tweets from the API
        """
        if const.TWITTER_API == 'python-twitter':
            return PythonTweets(tweets)
        else:
            raise ValueError(const.TWITTER_API)

class PythonTweets(object):
    """Handles tweet from `Status` object of `python-twitter` mudule

    Attributes:
    ----------
    - `tweets`: a list of `twitter.Status` objects, each representing a single tweet.

    Methods:
    --------
    - `format_attributes(self, interesting_attributes)``: run every method to
       format attributes which are in `interesting_attributes` list
    - `extract_user_name(self)`: extracts the screen name from the object User.
    - `convert_timestamp_created_at(self)`: converts `created_at` attribute
      in a proper timestamp.
    - `preprocess_tweet_text(self, text)`: cleans tweet text.
    - `format_user(self)`: formats `user` attribute.
    - `format_created_at(self)`: formats `created_at` attribute.
    - `format_text(self)`: formats `text` attribute.
    - `format_full_text(self)`: formats `full_text` attribute.
    - `format_cleaned_text(self)`: formats `cleaned_text` attribute.
    - `format_hashtags(self)`: formats `hashtags` attribute.
    - `format_geo(self)`: formats `geo` attribute.
    - `format_media(self)`: formats `media` attribute.
    """

    def __init__(self, tweets):
        self.tweets = tweets
        self.formatting_defined_attributes = ['user', 'text', 'full_text', 'cleaned_text', 'created_at', 'hashtags', 'media', 'geo']

    def format_attributes(self, interesting_attributes):
        """For each interesting attribute,
        the function calls the appropriate format method"""
        for attribute in interesting_attributes:
            if attribute in self.formatting_defined_attributes:
                eval('self.format_{}()'.format(attribute))
        return self.tweets

    def preprocess_tweet_text(self, text):
        """Cleans tweet text using `tweet-preprocessor` module.
        At the moment, it removes url, hashtags, emoji, mentions and smileys
        from the original `full_text`"""
        prep.set_options(prep.OPT.URL, prep.OPT.EMOJI, prep.OPT.MENTION, prep.OPT.SMILEY)
        text = prep.clean(text)
        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
        text = text.replace('#', '')
        text = text.replace('RT : ', '')
        return text


    def format_text(self):
        """Formats `text` attribute, removing newlines."""
        for tweet in self.tweets:
            if tweet is not None and tweet.text is not None:
                tweet.text = tweet.text.replace('\r\n', ' ')
                tweet.text = tweet.text.replace('\n', ' ')
                tweet.text = tweet.text.replace('\r', ' ')
                tweet.text = tweet.text.replace(',', '')


    def format_full_text(self):
        """Formats `full_text` attribute, removing newlines."""
        for tweet in self.tweets:
            if tweet is not None and tweet.full_text is not None:
                tweet.full_text = tweet.full_text.replace('\r\n', ' ')
                tweet.full_text = tweet.full_text.replace('\n', ' ')
                tweet.full_text = tweet.full_text.replace('\r', '')
                tweet.full_text = tweet.full_text.replace(',', '')


    def format_cleaned_text(self):
        """Cleans `full_text` attribute and adds `cleaned_text` attribute,
        removing newlines and calling method `preprocess_tweet_text` on each
        `tweet.full_text` string."""
        for tweet in self.tweets:
            if tweet is not None and tweet.full_text is not None:
                tweet.cleaned_text = tweet.full_text.replace('\r\n', ' ')
                tweet.cleaned_text = tweet.cleaned_text.replace('\n', ' ')
                tweet.cleaned_text = tweet.cleaned_text.replace('\r', '')
                tweet.cleaned_text = tweet.cleaned_text.replace(',', '')
                tweet.cleaned_text = self.preprocess_tweet_text(tweet.cleaned_text.encode('utf-8'))


    def format_created_at(self):
        """Formats `created_at` attribute, adding that to the records"""
        self.convert_timestamp_created_at()

    def convert_timestamp_created_at(self):
        """Converts `created_at` attribute in timestamp."""
        for tweet in self.tweets:
            tuple_timestamp = time.strptime(tweet.created_at,
                                            const.CREATED_AT_OLD_FORMAT)
            tweet.created_at = time.strftime(const.CREATED_AT_NEW_FORMAT,
                                             tuple_timestamp)


    def format_hashtags(self):
        """Formats `hashtags` attribute, converting a list to a concatenation
        of strings."""
        for tweet in self.tweets:
            hashtags_list = []
            for hashtag in tweet.hashtags:
                hashtags_list.append(hashtag.text)
            tweet.hashtags = ', '.join(hashtags_list)


    def format_urls(self):
        """Formats `urls` attribute, converting a list to a concatenation
        of strings."""
        for tweet in self.tweets:
            urls_list = []
            for url in tweet.urls:
                urls_list.append(url.expanded_url)
            tweet.urls = ', '.join(urls_list)

    def format_geo(self):
        """Formats `geo` attribute. Creates attributes 'lat' and 'lon'."""
        for tweet in self.tweets:
            if tweet.geo is not None:
                tweet.geo = '{}, {}'.format(tweet.geo['coordinates'][0], tweet.geo['coordinates'][1])
            else:
                tweet.geo = None

    def format_media(self):
        """Formats `media` attribute, converting a list to a concatenation
        of strings."""
        for tweet in self.tweets:
            media_list = []
            if tweet.media and len(tweet.media) > 0:
                for media in tweet.media:
                    media_list.append(media.media_url_https)
                tweet.media = ', '.join(media_list)

    def format_user(self):
        """Format `user` attribute, adding that to the tweet object"""
        self.extract_user_name()

    def extract_user_name(self):
        """Extracts the screen name from the object User."""
        for tweet in self.tweets:
            tweet.user = tweet.user.screen_name

    def get_only_interesting_attributes(self):
        """Isolates just the interesting attributes of the tweets.
        Interesting attributes are defined in `ATTR_FILE_INI`.
        If `clean_flag` is True, a custom column is added to
        `interesting_attributes` called `cleaned_text`.
        If `geo` is in `interesting_attributes`, two custom column are added to
        `interesting_attributes` called `lat` and `lon`."""
        if 'user' in self.interesting_attributes:
            self.extract_user_name()
        if 'created_at' in self.interesting_attributes:
            self.convert_timestamp_created_at()
        if 'text' in self.interesting_attributes:
            self.format_text()
        if 'full_text' in self.interesting_attributes:
            self.format_full_text()
            if self.clean_flag:
                self.format_cleaned_text()
                self.interesting_attributes.append('cleaned_text')
        if 'hashtags' in self.interesting_attributes:
            self.format_hashtags()
        if 'urls' in self.interesting_attributes:
            self.format_urls()
        if 'media' in self.interesting_attributes:
            self.format_media()
        if 'geo' in self.interesting_attributes:
            self.format_geo()
            self.interesting_attributes.remove('geo')
            self.interesting_attributes.append('lat')
            self.interesting_attributes.append('lon')
        logging.debug('Getting attributes: {}'
                     .format(self.interesting_attributes))
        records = [{key: getattr(tweet, key)
                    for key in self.interesting_attributes}
                   for tweet in self.tweets]
        return records


class MockTweet(object):
    """Still not used"""

    def __init__(self, tweet_dict):
        self.created_at = tweet_dicts['created_at']
        self.user = tweet_dicts['user']
        self.text = tweet_dicts['text']
        self.full_text = tweet_dicts['full_text']
        self.favorite_count = tweet_dicts['favorite_count']
        self.retweet_count = tweet_dicts['retweet_count']
        self.hashtags = tweet_dicts['hashtags']
        self.urls = tweet_dicts['urls']
        self.geo = tweet_dicts['geo']
