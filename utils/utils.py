import logging
import os
import constants as const

def validate_args(args):
    """Validates the arguments using the following rules:
    - length 'query_word' must be less than 15 characters if 'by-user'
    - 'query_word' must be a valid file if 'search_type' is one of by list
    - 'out_dir' must be an existing directory
    - 'ntweets' must be a positive number
    - 'nseconds' must be a positive number
    """
    args_are_not_valid = validate_search_type(args) or validate_query_word(args) or validate_out_dir(args.out_dir) or validate_ntweets(args.ntweets) or validate_nseconds(args.nseconds)
    if args_are_not_valid:
        return False
    else:
        logging.debug('Input parameters has been validated')
        return True

def validate_query_word(args):
    not_valid_args = args.query_word == None or validate_query_word_by_user(args) or validate_query_word_for_list(args)
    if not_valid_args:
        logging.error('ERROR: \'{}\' is not a valid query word'
                      .format(args.query_word))
    return not_valid_args

def validate_search_type(args):
    search_type_none = args.search_type == None
    if search_type_none:
        logging.error('ERROR: search_type not provided')
        return search_type_none
    if args.search_type == 'by-user':
        if args.subsearch_type:
            if args.subsearch_type != 'with-keyword':
                return True
            else:
                if args.subquery_word is None or args.subquery_word == '':
                    return True
        else:
            if args.subquery_word:
                return True
    return False

def validate_query_word_by_user(args):
    return args.query_word and len(args.query_word) > const.TWEET_MAX_LEN and args.search_type == 'by-user'

def validate_query_word_for_list(args):
    return args.query_word and args.search_type in ['by-users-list', 'by-keywords-list'] and not os.path.exists(args.query_word)

def validate_out_dir(out_dir):
    not_valid_args = out_dir and os.path.isdir(out_dir) == False
    if not_valid_args:
        logging.error('ERROR: \'{}\' is not an existing directory'
                .format(out_dir))
    return not_valid_args

def validate_ntweets(ntweets):
    not_valid_args = ntweets and (not ntweets.isdigit() or ntweets < 0)
    if not_valid_args:
        logging.error('ERROR: \'{}\' is not a valid value for --number-of-tweets'
                .format(ntweets))
    return not_valid_args

def validate_nseconds(nseconds):
    not_valid_args = nseconds and (not nseconds.isdigit() or nseconds < 0)
    if not_valid_args:
        logging.error('ERROR: \'{}\' is not a valid value for --repeat-every'
                .format(nseconds))
    return not_valid_args
