"""Constants for the package 'tweets_handler'"""
CRED_FILE_INI = './tweets_handler/resources/twitter_api_credentials.ini' # path to twitter_api_credentials.ini
HASHTAG_SYMBOL = '%23' # hashtag unicode symbol
MAX_COUNT_KEYWORD = 100 # max tweet retrieved by keyword
MAX_COUNT_USER = 200 # max tweet retrieved by user
INCLUDE_ENTITIES = True # include entitiees or not from the retrieved tweets
EXCLUDE_REPLIES = False # exclude replies or not from retrieved tweets
GET_TWEETS_BY = {'by-keyword': 'self.get_tweets_by_keyword()',
                 'by-user': 'self.get_tweets_by_user()',
                 'by-keywords-list': 'self.get_tweets_by_list_of_keywords()',
                 'by-users-list': 'self.get_tweets_by_list_of_users()'}
