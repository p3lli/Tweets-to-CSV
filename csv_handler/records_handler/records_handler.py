import configparser
import time
import datetime
import logging
import preprocessor as prep
import html
import constants as const


class RecordsHandler(object):
    """Handles collection of tweets as records for the CSV file."""


    def __init__(self, tweets, clean_flag):
        self.tweets = tweets
        self.clean_flag = clean_flag
        config = configparser.ConfigParser()
        config.read(const.ATTR_FILE_INI)
        config_attributes = config['interesting-attributes']['attrs']
        self.interesting_attributes = config_attributes.split(',')


    def extract_user_name(self):
        """Extracts the screen name from the object User."""
        for tweet in self.tweets:
            tweet.user = tweet.user.screen_name


    def convert_timestamp_created_at(self):
        """Converts 'created_at' attribute in timestamp."""
        for tweet in self.tweets:
            tuple_timestamp = time.strptime(tweet.created_at,
                                            const.CREATED_AT_OLD_FORMAT)
            tweet.created_at = time.strftime(const.CREATED_AT_NEW_FORMAT,
                                             tuple_timestamp)


    def preprocess_tweet_text(self, text):
        """Cleans tweet text using 'tweet-preprocessor' module"""
        prep.set_options(prep.OPT.URL, prep.OPT.EMOJI, prep.OPT.MENTION, prep.OPT.SMILEY)
        text = prep.clean(text)
        text = text.replace('#', '')
        text = text.replace('RT : ', '')
        return text


    def format_text(self):
        """Formats 'text' attribute."""
        for tweet in self.tweets:
            if tweet is not None and tweet.text is not None:
                tweet.text = tweet.text.replace('\r\n', ' ')
                tweet.text = tweet.text.replace('\n', ' ')
                tweet.text = tweet.text.replace('\r', ' ')
                tweet.text = tweet.text.replace(',', '')


    def format_full_text(self):
        """Formats 'full_text' attribute."""
        for tweet in self.tweets:
            if tweet is not None and tweet.full_text is not None:
                tweet.full_text = tweet.full_text.replace('\r\n', ' ')
                tweet.full_text = tweet.full_text.replace('\n', ' ')
                tweet.full_text = tweet.full_text.replace('\r', '')
                tweet.full_text = tweet.full_text.replace(',', '')


    def format_cleaned_text(self):
        """Cleans 'full_text' attribute and adds 'cleaned_text' attribute."""
        for tweet in self.tweets:
            if tweet is not None and tweet.full_text is not None:
                tweet.cleaned_text = tweet.full_text.replace('\r\n', ' ')
                tweet.cleaned_text = tweet.cleaned_text.replace('\n', ' ')
                tweet.cleaned_text = tweet.cleaned_text.replace('\r', '')
                tweet.cleaned_text = tweet.cleaned_text.replace(',', '')
                tweet.cleaned_text = self.preprocess_tweet_text(tweet.cleaned_text.encode('utf-8'))


    def format_hashtags(self):
        """Formats 'hashtags' attribute."""
        for tweet in self.tweets:
            hashtags_list = []
            for hashtag in tweet.hashtags:
                hashtags_list.append(hashtag.text)
            tweet.hashtags = ', '.join(hashtags_list)


    def format_urls(self):
        """Formats 'urls' attribute."""
        for tweet in self.tweets:
            urls_list = []
            for url in tweet.urls:
                urls_list.append(url.expanded_url)
            tweet.urls = ', '.join(urls_list)

    def format_geo(self):
        """Formats 'geo' attribute. Creates attributes 'lat' and 'lon'"""
        for tweet in self.tweets:
            if tweet.geo is not None:
                tweet.lat = tweet.geo['coordinates'][0]
                tweet.lon = tweet.geo['coordinates'][1]
            else:
                tweet.lat = None
                tweet.lon = None

    def format_media(self):
        """Formats 'media' attribute."""
        for tweet in self.tweets:
            media_list = []
            if tweet.media and len(tweet.media) > 0:
                for media in tweet.media:
                    media_list.append(media.media_url_https)
                tweet.media = ', '.join(media_list)


    def get_only_interesting_attributes(self):
        """Isolates just the interesting attributes of the tweets."""
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
