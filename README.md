# Tweets in CSV with python

This small project has been made to collect tweets using Twitter API and then store them in a CSV file.  
At the moment, tweets are gathered based on keywords or directly from a specific account.  

## Config file (.ini)
### Twitter API
The project uses [python-twitter](https://github.com/bear/python-twitter) to connect with the Twitter API.  
To run the project, you must first obtain all the API credentials, using a Twitter Account.  
Follow the instructions at [https://apps.twitter.com/](https://apps.twitter.com/) to get:  

* A Consumer Key
* A Consumer Secret
* An Access Token Key
* An Access Token Secret

You have to create an `.ini` file in `twitter_handler/resources` called `twitter_api_credentials.ini`.  
The file format is showed in `twitter_handler/resources/twitter_api_credentials_example.ini`.  

### CSV Header
A tweet is representend by a `twitter.models.Status` object from the `python-twitter` module.  
For a complete list of the attributes associated to a tweet, visit the [documentation](http://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status).  
You can set the attributes to be exported in `csv_handler/resources/interesting_attributes.ini`.  
At the moment, the following attributes are guaranteed to be supported:  
* `created_at`
* `text`
* `user`

## Initialization
To initialize the project, create a virtual environment with `virtualenv`.  
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

### Usage
The project entry point is in `main.py`.  
```
usage: main.py [-h] [-v] search_type query_word out_dir

Script made to gather tweets and store them in a CSV file.

positional arguments:
  search_type    Specifies the type of search to be performed.
                 Values accepted:
                 -'by-keyword'
                 -'by-user'
  query_word     A keyword or a username to be used in the search.
  out_dir        Directory where the CSV file will be saved.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Increases log verbosity.

```
