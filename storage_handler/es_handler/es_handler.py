
class ElasticsearchHandler(object):

    def __init__(self, args, tweets_handler):
        self.args = args
        self.tweets_handler = tweets_handler

    def store(self):
        """Interface method for StorageHandler"""
        # TODO
        return True
