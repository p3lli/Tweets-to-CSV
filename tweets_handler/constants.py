"""Constants for the package 'tweets_handler'"""
CRED_FILE_INI = './tweets_handler/resources/twitter_api_credentials.ini'
HASHTAG_SYMBOL = '%23'
MAX_COUNT_KEYWORD = 100
MAX_COUNT_USER = 200
INCLUDE_ENTITIES = True
EXCLUDE_REPLIES = False
GET_TWEETS_BY = {'by-keyword': 'self.get_tweets_by_keyword()',
                 'by-user': 'self.get_tweets_by_user()',
                 'by-keywords-list': 'self.get_tweets_by_list_of_keywords()',
                 'by-users-list': 'self.get_tweets_by_list_of_users()'}
