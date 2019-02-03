# Tweets in CSV with python

This small project has been made to collect tweets using Twitter API and then store them in a CSV file.  
At the moment, tweets are gathered based on keywords or directly from a specific account.  

## Preface
I do realize that the script has been used more extensively by _non computer scientists_.  
Because of that, I am trying to be more explanatory and _verbose_ in this README.  
Please, give me any feedback to improve clearness and correctness of this part.  
Thank you  

## Config file (.ini)
### Twitter API
The project uses [python-twitter](https://github.com/bear/python-twitter) module to connect with the Twitter API.  
To run the project, you must first obtain all the API credentials, using a valid Twitter Account.  
Follow the instructions at [https://apps.twitter.com/](https://apps.twitter.com/) to get:  

* A Consumer Key
* A Consumer Secret
* An Access Token Key
* An Access Token Secret

You have to create an `.ini` file in `tweets_handler/resources` called `twitter_api_credentials.ini`.  
The file format is showed in `tweets_handler/resources/twitter_api_credentials_example.ini`.  

### CSV Header
A tweet is representend by a `twitter.models.Status` object from the `python-twitter` module.  
For a complete list of the attributes associated to a tweet, visit the [documentation](http://python-twitter.readthedocs.io/en/latest/_modules/twitter/models.html#Status).  
You can set the attributes to be exported in `csv_handler/resources/interesting_attributes.ini`.  
At the moment, the following attributes are guaranteed to be supported:  
* `created_at`
* `full_text`
* `user`
* `favorite_count`
* `retweet_count`
* `hashtags`
* `urls`
* `geo`

## Initialization
To initialize the project, create a virtual environment with `virtualenv`
inside the project directory.  
To install `virtualenv` in Linux:  
```
sudo apt-get install python-pip python-dev build-essential
pip install virtualenv
```
or in MacOS:  
```
brew install python
pip install virtualenv
```

After the installation, change directory to the project directory:  
```
cd  /path/to/Tweets-to-CSV
```

and execute:  
```
virtualenv --python=$(which python2) env-twi
```

Now, activate the virtual environment inside the project directory:  
```
source env-twi/bin/activate
```

Then install the required modules:  
```
pip install -r requirements.txt
```

## Project Structure
Here is the project structure. It consists of three subpackages for handling tweets, csv and general  
utilities. Inside the csv subpackage there is a subsubpackage for handling single records.  
Every subpackage has a module 'constants.py' containing any constant variable specific to that subpackage.  
```
Tweets-to-CSV
├── main.py
├── README.md
├── requirements.txt
├── csv_handler
│   ├── constants.py
│   ├── csv_handler.py
│   ├── __init__.py
│   ├── records_handler
│   │   ├── constants.py
│   │   ├── __init__.py
│   │   └── records_handler.py
│   └── resources
│       └── interesting_attributes.ini
├── tweets_handler
│   ├── constants.py
│   ├── __init__.py
│   ├── resources
│   │   ├── twitter_api_credentials_example.ini
│   │   └── twitter_api_credentials.ini
│   └── tweets_handler.py
└── utils
    ├── constants.py
    ├── __init__.py
    └── utils.py
```

## Usage
The project entry point is in `main.py`.  
```
usage: main.py [-h] [-v] search_type query_word out_dir

Script made to gather tweets and store them in a CSV file.

positional arguments:
  search_type    Specifies the type of search to be performed.
                 Values accepted:
                 -'by-keyword'
                 -'by-user'
                 -'by-keywords-list'
                 -'by-users-list'
  query_word     A keyword or a username to be used in the search.
                 If selecting 'by-keywords-list' or 'by-users-list',
                 'query_word' must be a text file like 'keywords_list.txt'.
  out_dir        Directory where the CSV file will be saved.

optional arguments:
  -h, --help     show this help message and exit
  -a, --append   Appends tweets to a compatible CSV (same search, different time).
  -c, --clean    Adds a custom column 'cleaned_text' in which text is cleaned
                 by emoji, smiley, url and mentions.
  -v, --verbose  Increases log verbosity.


```
