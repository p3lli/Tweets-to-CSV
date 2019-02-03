"""Script made to gather tweets and store them in a CSV file."""
import sys
import os
import logging
import argparse
from argparse import RawTextHelpFormatter
from tweets_handler import ApiHandler
from csv_handler import CSVFileHandler
from utils import validate_args


def main(args):
    """Main entry point for the script.

    - Validation of the arguments.
    - First communication with the Twitter API using the credentials.
    - Retrieving of the tweets as a list of `twitter.Status` objects.
    - Processing of the tweets and transformation to a list of dictionaries.
    - CSV file export."""
    logging.info('Starting script'.format(args.query_word))
    logging.debug('Input parameters: \'{}\', \'{}\', \'{}\''
                  .format(args.search_type, args.query_word, args.out_dir))
    if validate_args(args):
        api_handler = ApiHandler(args.query_word, args.search_type)
        tweets = api_handler.get_tweets()
        csv_handler = CSVFileHandler(args.query_word, args.search_type,
                                    args.out_dir, args.append_to, args.clean,
                                    tweets)
        csv_handler.export_csv()
    else:
        logging.info('Script stopped')


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
    parser.add_argument('-a', '--append', dest='append_to', action='store_true',
            help='Appends tweets to a compatible CSV (same search, different time).')
    parser.add_argument('-c', '--clean', dest='clean', action='store_true',
            help='Adds a custom column \'cleaned_text\' in which text is cleaned\n'
            + 'by emoji, smiley, url and mentions.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Increases log verbosity.')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    logging_level = logging.INFO
    if args.verbose:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level,
            format='%(asctime)-15s %(message)s')
    main(args)
