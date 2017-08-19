"""Script to gather tweets based on hashtags and store them in a CSV file."""
import sys
import argparse
import logging

def main(args):
    """Main entry point for the script."""
    pass

def get_parser():
    """Defines the parser object for argparse"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query_word', metavar='query_word', type=str,
            help='Hashtag content for the main query (no \'#\' included).')
    parser.add_argument('out_dir', metavar='out_dir', type=str,
            help='Directory where the CSV file will be saved.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', 
            help='Increase ouput verbosity.')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    logging_level = logging.INFO
    if args.verbose:
        logging_level = logging.DEBUG
    logging.basicConfig(level=logging_level, 
            format='%(asctime)-15s %(module)s.%(funcName)s: %(message)s')
    main(args)
