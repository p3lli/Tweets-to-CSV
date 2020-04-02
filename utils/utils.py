import os
import logging
import constants as const

def validate_args(args):
    """Validates the arguments using the following rules:
    - length 'query_word' must be less than 15 characters if 'by-user'
    - 'out_dir' must be an existing directory
    """
    valid_args = True
    if args.query_word and len(args.query_word) > const.TWEET_MAX_LEN and args.search_type == 'by-user':
        valid_args = False
        logging.error('ERROR: \'{}\' is not a valid user name'
                      .format(args.query_word))
    if args.out_dir and os.path.isdir(args.out_dir) == False:
        valid_args = False
        logging.error('ERROR: \'{}\' is not an existing directory'
                .format(args.out_dir))
    if args.ntweets and (not args.ntweets.isdigit() or args.ntweets < 0):
        valid_args = False
        logging.error('ERROR: \'{}\' is not a valid value for --number-of-tweets'
                .format(args.ntweets))
    if args.nseconds and (not args.nseconds.isdigit() or args.nseconds < 0):
        valid_args = False
        logging.error('ERROR: \'{}\' is not a valid value for --repeat-every'
                .format(args.nseconds))
    if valid_args:
        logging.debug('Input parameters has been validated')
    return valid_args
