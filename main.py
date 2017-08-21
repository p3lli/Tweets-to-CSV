"""Script made to gather tweets and store them in a CSV file."""
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import logging
from tweets_handler import ApiHandler
from csv_handler import RecordsHandler

def main(args):
    """Main entry point for the script."""
    logging.info('Starting script'.format(args.query_word))
    logging.debug('Input parameters: \'{}\', \'{}\', \'{}\''
                  .format(args.search_type, args.query_word, args.out_dir))
    if validate_args(args):
        api_handler = ApiHandler(args.query_word, args.search_type)
        tweets = api_handler.get_tweets()
        records_handler = RecordsHandler(tweets)
        print records_handler.get_only_interesting_attributes()

    else:
        logging.info('Script stopped')


def get_parser():
    """Defines the parser object for argparse."""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('search_type', metavar='search_type', type=str,
            choices=['by-keyword', 'by-user'],
            help='Specifies the type of search to be performed.\n'
            + 'Values accepted:\n'
            + '-\'by-keyword\'\n'
            + '-\'by-user\'\n')
    parser.add_argument('query_word', metavar='query_word', type=str,
            help='A keyword or a username to be used in the search.')
    parser.add_argument('out_dir', metavar='out_dir', type=str,
            help='Directory where the CSV file will be saved.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
            help='Increases log verbosity.')
    return parser


def validate_args(args):
    """Validates the arguments using the following rules:
    - length 'query_word' must be less than 15 characters if 'by-user'
    - 'out_dir' must be an existing directory"""
    valid_args = True
    if len(args.query_word) > 15 and args.search_type == 'by-user':
        valid_args = False
        logging.error('ERROR: \'{}\' is not a valid user name'
                      .format(args.query_word))
    if os.path.isdir(args.out_dir) == False:
        valid_args = False
        logging.error('ERROR: \'{}\' is not an existing directory'
                .format(args.out_dir))
    if valid_args:
        logging.debug('Input parameters has been validated')
    return valid_args


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    logging_level = logging.INFO
    if args.verbose:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level,
            format='%(asctime)-15s %(message)s')
    main(args)
