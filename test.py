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
                                                 True)}


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
