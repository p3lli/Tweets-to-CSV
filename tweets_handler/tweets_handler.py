import logging

def get_tweets(args):
    """Gets tweets containing a specific hashtag"""
    logging.debug("Getting tweets with hashtag: #{}".format(args.query_word))
