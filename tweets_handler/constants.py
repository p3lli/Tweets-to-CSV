"""Constants for the package 'tweets_handler'"""
CRED_FILE_INI = './tweets_handler/resources/twitter_api_credentials.ini' # path to twitter_api_credentials.ini
HASHTAG_SYMBOL = '%23' # hashtag unicode symbol
MAX_NUMBER_OF_TWEETS = 200 # max number of tweets retrieved
INCLUDE_ENTITIES = True # include entitiees or not from the retrieved tweets
EXCLUDE_REPLIES = False # exclude replies or not from retrieved tweets
GET_TWEETS_BY = {'by-keyword': 'self.get_tweets_by_keyword()',
                 'by-user': 'self.get_tweets_by_user()',
                 'by-keywords-list': 'self.get_tweets_by_list_of_keywords()',
                 'by-users-list': 'self.get_tweets_by_list_of_users()'}
