import pytest
from twitter_api_handler import ApiHandler

test_tweets = [
{'created_at': '2019-01-10T20:00:00Z', 'user': 'user1',
'text': 'this is some text, banana',
'full_text': 'this is some full text, banana #banana',
'favorite_count': '42',
'retweet_count': '42',
'hashtag': '#banana',
'urls': 'https://banana.bz/'
},
{'created_at': '2019-01-14T18:30:00Z', 'user': 'user1',
'text': 'this is some other text, banana',
'full_text': 'this is some other full text, banana #banana',
'favorite_count': '42',
'retweet_count': '42',
'hashtag': '#banana',
'urls': 'https://banana.bz/'
},
{'created_at': '2019-01-29T20:00:00Z', 'user': 'user1',
'text': 'this is some text, ananas',
'full_text': 'this is some full text, ananas #ananas',
'favorite_count': '42',
'retweet_count': '42',
'hashtag': '#ananas',
'urls': 'https://banana.bz/'
},
{'created_at': '2020-04-02T12:30:00Z', 'user': 'user2',
'text': 'I am also saying banana',
'full_text': 'I am also saying a full text banana #banana',
'favorite_count': '42',
'retweet_count': '42',
'hashtag': '#banana',
'urls': 'https://banana.bz/'
}
]

class APIHandlerArgsTestCase():
    def __init__(self, query_word, search_type, ntweets, ntweets_retrieved):
        self.query_word = query_word
        self.search_type = search_type
        self.ntweets = ntweets
        self.ntweets_retrieved = ntweets_retrieved


def test_get_tweets_by_keyword():
    cases = {
        "retrieve_all_tweets": APIHandlerArgsTestCase('banana',
                                                    'by-keyword',
                                                    200,
                                                    3),
        "retrieve_just_one_tweet": APIHandlerArgsTestCase('banana',
                                                    'by-keyword',
                                                    1,
                                                    1),
        "no_tweets_with_keyword": APIHandlerArgsTestCase('mango',
                                                    'by-keyword',
                                                    100,
                                                    0)}
    for key in cases:
        api_handler = ApiHandler(cases[key], 'mock', test_tweets)
        results = api_handler.get_tweets_by_keyword()
        assert len(results) == cases[key].ntweets_retrieved


def test_get_tweets_by_user():
    cases = {
        "retrieve_all_tweets": APIHandlerArgsTestCase('user1',
                                                    'by-user',
                                                    200,
                                                    3),
        "retrieve_just_one_tweet": APIHandlerArgsTestCase('user1',
                                                    'by-user',
                                                    1,
                                                    1),
        "no_tweets_with_keyword": APIHandlerArgsTestCase('user3',
                                                    'by-user',
                                                    100,
                                                    0)}
    for key in cases:
        api_handler = ApiHandler(cases[key], 'mock', test_tweets)
        results = api_handler.get_tweets_by_user()
        assert len(results) == cases[key].ntweets_retrieved
