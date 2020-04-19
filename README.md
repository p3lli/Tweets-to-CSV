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

1) After the installation, change directory to the project directory:  
```
cd  /path/to/Tweets-to-CSV
```

2) The script still runs with python2. Execute:  
```
virtualenv --python=$(which python2) env-twi
```

3) Now, activate the virtual environment inside the project directory:  
```
source env-twi/bin/activate
```

4) Execute:
```
python --version
```

5) If the version is different from 2, delete folder `env-twi` and try this command:

```
virtualenv --python=$(which python2.7) env-twi
```

Activate the virtual environment (3) and check python version (4)

6) Then install the required modules:  
```
pip install -r requirements.txt
```

## Tests
I am slowly adding tests to the scripts.
I know this is not the right process and it is against TDD, but unfortunately
I started this project way before I knew TDD even exists.

To run tests:
```
pytest
```

Make sure to execute tests before pushing a new commit
(I am also talking to myself)

## Elasticsearch configuration
Following the guide [Running the Elastic Stack on Docker](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html#get-started-docker-tls)

## Project Structure
Here is the project structure. It consists of three subpackages for handling tweets, csv and general  
utilities. Inside the csv subpackage there is a subsubpackage for handling single records.  
Every subpackage has a module 'constants.py' containing any constant variable specific to that subpackage.  
```
Tweets-to-CSV

├── api_handler
│   ├── constants.py
│   ├── __init__.py
│   ├── resources
│   │   ├── twitter_api_credentials_example.ini
│   │   └── twitter_api_credentials.ini
│   ├── tweets_handler.py
│   ├── twitter_api_handler.py
│   └── twitter_api_wrapper.py
├── keywords_list.txt
├── main.py
├── README.md
├── requirements.txt
├── storage_handler
│   ├── csv_handler
│   │   ├── constants.py
│   │   ├── csv_handler.py
│   │   ├── __init__.py
│   │   ├── records_handler
│   │   │   ├── constants.py
│   │   │   ├── __init__.py
│   │   │   └── records_handler.py
│   │   └── resources
│   │       └── interesting_attributes.ini
│   ├── es_handler
│   │   ├── es_handler.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── storage_handler.py
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
  -h, --help     show this help message and exit.
  -s {CSV}, --storage-type {CSV}
                  Specifies which type of storage to use.
                  Values accepted:
                  -'CSV'
                  -'ES'
  -n NTWEETS, --number-of-tweets NTWEETS
                 Set the amount of tweets to be retrieved.
  -a, --append   Appends tweets to a compatible CSV (same search, different time).
  -r NSECONDS, --repeat-every NSECONDS
                 Repeats the same search every NSECONDS
  -c, --clean    Adds a custom column 'cleaned_text' in which text is cleaned
                 by emoji, smiley, url and mentions.
  -v, --verbose  Increases log verbosity.


```

### Examples
- `python main.py by-keyword banana /path/to/destination/directory`
It retrieves tweets by keyword `banana` and stores them in a CSV
named `tweets_with_banana_TIMESTAMP.csv` in the `/path/to/destination/directory`
directory.

- `python main.py by-user ThePSF /path/to/destination/directory`
It retrieves tweets from user `ThePSF` and stores them in a CSV
named `tweets_by_ThePSF_TIMESTAMP.csv` in the `/path/to/destination/directory`
directory.

- `python main.py by-keywords-list path/to/keywords-list.txt /path/to/destination/directory`
It retrieves tweets containing keywords specified in `/path/to/keywords-list.txt`
and stores them in a CSV  named `tweets_tweets_from_keywords_list_TIMESTAMP.csv`
in the `/path/to/destination/directory` directory.
