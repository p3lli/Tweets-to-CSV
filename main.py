"""Script made to gather tweets and store them in a CSV file."""
import argparse
import logging
import os
import sys
import time
from argparse import RawTextHelpFormatter
from api_handler import ApiHandler
from storage_handler import StorageHandler
from utils import validate_args


def main(args):
    """Main entry point for the script.

    - Validation of the arguments.
    - First communication with the Twitter API using the credentials.
    - Retrieving of the tweets as a list of `twitter.Status` objects.
    - Processing of the tweets and transformation to a list of dictionaries.
    - CSV file export."""
    logging.info('Starting script'.format(args.query_word))
    logging.debug('Input parameters: \'{}\''.format(repr(args)))
    if validate_args(args):
        main_loop(args)
    else:
        logging.info('Script stopped')


def main_loop(args):
    twitter_api_handler = ApiHandler(args)
    while args.nseconds:
        retrieve_and_store_tweets(args, twitter_api_handler)
        logging.info('Waiting {} seconds for next search...'.format(args.nseconds))
        time.sleep(float(args.nseconds))
    # TODO add a more elegant way to interrupt the cycle (more than CTRL+C)
    retrieve_and_store_tweets(args, twitter_api_handler)


def retrieve_and_store_tweets(args, twitter_api_handler):
    tweets_handler = twitter_api_handler.get_tweets()
    storage_handler = StorageHandler(args, tweets_handler)
    storage_handler.store()


def get_parser():
    """Defines the parser object for argparse."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('search_type', metavar='search_type', type=str,
            choices=['by-keyword', 'by-user', 'by-keywords-list', 'by-users-list'],
            help='Specifies the type of search to be performed.\n'
            + 'Values accepted:\n'
            + '-\'by-keyword\'\n'
            + '-\'by-user\'\n'
            + '-\'by-keywords-list\'\n'
            + '-\'by-users-list\'\n')
    parser.add_argument('query_word', metavar='query_word', type=str,
            help='A keyword or a username to be used in the search.\n'
            + 'If selecting \'by-keywords-list\' or \'by-users-list\', \n'
            + '\'query_word\' must be a text file like \'keywords_list.txt\'.')
    parser.add_argument('out_dir', metavar='out_dir', type=str,
            help='Directory where the CSV file will be saved.')
    parser.add_argument('-wk', '--with-keyword', dest='subquery_word',
            help='A keyword to filter tweets from user (to be used with \'by-user\')')
    parser.add_argument('-s', '--storage-type', dest='storage_type',
            choices=['CSV'], default='CSV',
            help='Specifies which type of storage to use.\n'
            + 'Values accepted:\n'
            + '-\'CSV\'\n'
            + '-\'ES\'\n')
    parser.add_argument('-n', '--number-of-tweets', dest='ntweets',
            help='Set the amount of tweets to be retrieved')
    parser.add_argument('-a', '--append', dest='append_to', action='store_true',
            help='Appends tweets to a compatible CSV (same search, different time).')
    parser.add_argument('-r', '--repeat-every', dest='nseconds',
            help='Repeats the same search every NSECONDS')
    parser.add_argument('-c', '--clean', dest='clean', action='store_true',
            help='Adds a custom column \'cleaned_text\' in which text is cleaned\n'
            + 'by emoji, smiley, url and mentions.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Increases log verbosity.')
    return parser

def set_logging_level(args):
    logging_level = logging.INFO
    if args.verbose:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level,
            format='%(asctime)-15s %(message)s')


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    set_logging_level(args)
    main(args)
