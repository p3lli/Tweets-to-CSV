# Tweets in CSV with python

This small project has been made to collect tweets using Twitter API and then store them in a CSV file.  
At the moment, tweets are gathered based on keywords or from a specific account.  

### Twitter API
The project uses [python-twitter](https://github.com/bear/python-twitter) to connect with the Twitter API.  
To run the project, you must first obtain all the API credentials, using a Twitter Account.  
Follow the instructions at [https://apps.twitter.com/](https://apps.twitter.com/) to get:  

* A Consumer Key
* A Consumer Secret
* An Access Token Key
* An Access Token Secret

You have to create an .ini file in 'twitter_handler/resources' called 'twitter_api_credentials.ini'.  
The file format is showed in 'twitter_handler/resources/twitter_api_credentials_example.ini'.  

### Without a Makefile
To initialize the project, create a virtual environment with virtualenv. I have named mine 'env-twi'.  
```
virtualenv env-twi
```

Now, activate the virtual environment:  
```
source ./env-twi/bin/activate
```

Then install the required modules:  
```
pip install -r requirements.txt
```

###
