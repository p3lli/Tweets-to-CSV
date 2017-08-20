import pandas as pd

class RecordsHandler(object):
    """Handles collection of tweets."""

    def __init__(self, tweets,
                 interesting_attributes=['created_at',
                                         'user',
                                         'text']):
        self.tweets = tweets
        self.interesting_attributes = interesting_attributes

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
