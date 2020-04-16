import unittest
from utils import validate_args

class UnitTest(unittest.TestCase):

    def test_validate_args(self):
        cases = {
        "valid_arguments": TestCaseValidateArgs('banana',
                                                 'by-keyword',
                                                 '.',
                                                 100,
                                                 5,
                                                 True),
        "missing_search_type": TestCaseValidateArgs('banana',
                                                 None,
                                                 '.',
                                                 100,
                                                 5,
                                                 False),
        "missing_query_word": TestCaseValidateArgs(None,
                                                 'by-keyword',
                                                 '.',
                                                 100,
                                                 5,
                                                 False),
        "not_existing_dir": TestCaseValidateArgs('banana',
                                                 'by-keyword',
                                                 './not_existing_dir/',
                                                 100,
                                                 5,
                                                 False)}


class TestCaseValidateArgs():
    def __init__(self, query_word, search_type, out_dir, ntweets, nseconds, is_valid):
        self.query_word = query_word
        self.search_type = search_type
        self.out_dir = out_dir
        self.ntweets = ntweets
        self.nseconds = nseconds
        self.is_valid = is_valid
