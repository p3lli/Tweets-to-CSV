import pytest
from csv_handler import CSVFileHandler

class MockTweetHanlder(object):
    """TODO
    get_only_interesting_attributes returns an empty dictionary"""

    def format_attributes(self, interesting_attributes):
        return {}

class CSVHandlerArgsTestCase():
    def __init__(self, query_word, search_type, out_dir, append_to, clean, csv_file_name):
        self.query_word = query_word
        self.search_type = search_type
        self.out_dir = out_dir
        self.append_to = append_to
        self.csv_file_name = csv_file_name
        self.clean = clean

def test_name_csv_file():
    cases = {
        "tweets_with_mango": CSVHandlerArgsTestCase('mango',
                                                    'by-keyword',
                                                    '.',
                                                    False,
                                                    False,
                                                    'tweets_with_mango'),
        "tweets_by_mango": CSVHandlerArgsTestCase('mango',
                                                    'by-user',
                                                    '.',
                                                    False,
                                                    False,
                                                    'tweets_by_mango')
    }
    for key in cases:
        csv_handler = CSVFileHandler(cases[key], MockTweetHanlder())
        csv_file_name = csv_handler.name_csv_file()
        assert csv_file_name == cases[key].csv_file_name
