"""Script to gather tweets based on hashtags and store them in a CSV file."""
import sys
import os
import argparse
import logging
from tweets_handler import ApiHandler

def main(args):
    """Main entry point for the script."""
    logging.info('Starting script for hashtag #{}'.format(args.query_word))
    logging.debug('Running script verbosely')
    if validate_args(args):
        api_handler = ApiHandler(args.query_word)
        api_handler.get_tweets()
    else:
        logging.info('Script stopped')


def get_parser():
    """Defines the parser object for argparse."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query_word', metavar='query_word', type=str,
            help='Hashtag content for the main query (no \'#\' included).')
    parser.add_argument('out_dir', metavar='out_dir', type=str,
            help='Directory where the CSV file will be saved.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', 
            help='Increase ouput verbosity.')
    return parser


def validate_args(args):
    """Validates the arguments using the following rules:
    - 'query_word' must not have whitespaces
    - 'out_dir' must be an existing directory"""
    valid_args = True
    if ' ' in args.query_word:
        logging.error('ERROR: \'#{}\' is not a valid hashtag'.format(
            args.query_word))
        valid_args = False
    if os.path.isdir(args.out_dir) == False:
        logging.error('ERROR: \'{}\' is not an existing directory'
                .format(args.out_dir))
        valid_args = False
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
