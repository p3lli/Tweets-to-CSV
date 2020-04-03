
class ElasticsearchHandler(object):

    def __init__(self, args, tweets):
        self.args = args
        self.tweets = tweets

    def store(self):
        """Interface method for StorageHandler"""
        # TODO
        return True
