import unittest
from utils import validate_args

class UnitTest(unittest.TestCase):

    def test_validate_args(self):
        cases = {
        "valid_arguments": TestCaseValidateArgs('banana',
                                                 'by-keyword',
                                                 '.',
                                                 '100',
                                                 '5',
                                                 True),
        "too_long_username": TestCaseValidateArgs('banana_banana_banana_banana_banana_banana',
                                                 'by-user',
                                                 '.',
                                                 '100',
                                                 '5',
                                                 False),
        "missing_search_type": TestCaseValidateArgs('banana',
                                                 None,
                                                 '.',
                                                 '100',
                                                 '5',
                                                 False),
        "missing_query_word": TestCaseValidateArgs(None,
                                                 'by-keyword',
                                                 '.',
                                                 '100',
                                                 '5',
                                                 False),
        "negative_number_of_tweets": TestCaseValidateArgs('banana',
                                                 'by-keyword',
                                                 '.',
                                                 '-100',
                                                 '5',
                                                 False),
        "negative_number_of_seconds": TestCaseValidateArgs('banana',
                                                 'by-keyword',
                                                 '.',
                                                 '100',
                                                 '-5',
                                                 False),
        "not_existing_dir": TestCaseValidateArgs('banana',
                                                 'by-keyword',
                                                 './not_existing_dir/',
                                                 '100',
                                                 '5',
                                                 False)}

        for key in cases:
            is_valid = validate_args(cases[key])
            self.assertEqual(is_valid, cases[key].is_valid)


class TestCaseValidateArgs():
    def __init__(self, query_word, search_type, out_dir, ntweets, nseconds, is_valid):
        self.query_word = query_word
        self.search_type = search_type
        self.out_dir = out_dir
        self.ntweets = ntweets
        self.nseconds = nseconds
        self.is_valid = is_valid
