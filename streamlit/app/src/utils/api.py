import requests
from src.config import conf
from src.utils.database import Database
import time

def get_uri(uri):
    print("API URL")
    print(conf["api_url"])
    return conf["api_url"]+uri  
    
def predict_tweet(tweet, db):
    tweet_in_db = db.api.find_one({"content":tweet["content"]})
    print(tweet_in_db)
    if tweet_in_db and 'droite' in tweet_in_db:
        time.sleep(0.2)
        return tweet_in_db
    else:
        uri = get_uri('predict')
        res = requests.post(uri, data = tweet).json()
        return res

def predict_account(account_name):
    uri = get_uri('predict/account/{}'.format(account_name))
    res = requests.get(uri).json()
    return res

def get_tweets(account_name):
    uri = get_uri('tweets/{}'.format(account_name))
    res = requests.get(uri).json()
    return res


        
