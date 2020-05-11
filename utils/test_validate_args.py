import pytest
from utils import validate_args

def test_validate_args():
    cases = {
    "valid_arguments": ValidateArgsTestCase('banana',
                                             'by-keyword',
                                             '',
                                             '',
                                             '.',
                                             '100',
                                             '5',
                                             True),
    "too_long_username": ValidateArgsTestCase('banana_banana_banana_banana_banana_banana',
                                             'by-user',
                                             '',
                                             '',
                                             '.',
                                             '100',
                                             '5',
                                             False),
    "missing_search_type": ValidateArgsTestCase('banana',
                                             None,
                                             '',
                                             '',
                                             '.',
                                             '100',
                                             '5',
                                             False),
    "missing_query_word": ValidateArgsTestCase(None,
                                             'by-keyword',
                                             '',
                                             '',
                                             '.',
                                             '100',
                                             '5',
                                             False),
    "negative_number_of_tweets": ValidateArgsTestCase('banana',
                                             'by-keyword',
                                             '',
                                             '',
                                             '.',
                                             '-100',
                                             '5',
                                             False),
    "negative_number_of_seconds": ValidateArgsTestCase('banana',
                                             'by-keyword',
                                             '',
                                             '',
                                             '.',
                                             '100',
                                             '-5',
                                             False),
    "not_existing_dir": ValidateArgsTestCase('banana',
                                             'by-keyword',
                                             '',
                                             '',
                                             './not_existing_dir/',
                                             '100',
                                             '5',
                                             False)}

    for key in cases:
        is_valid = validate_args(cases[key])
        assert is_valid == cases[key].is_valid


class ValidateArgsTestCase():
    def __init__(self, query_word, search_type, subquery_word, subsearch_type, out_dir, ntweets, nseconds, is_valid):
        self.query_word = query_word
        self.search_type = search_type
        self.subquery_word = subquery_word
        self.subsearch_type = subsearch_type
        self.out_dir = out_dir
        self.ntweets = ntweets
        self.nseconds = nseconds
        self.is_valid = is_valid
