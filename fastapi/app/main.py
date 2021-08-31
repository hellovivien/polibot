from fastapi import FastAPI
import sys
sys.path.insert(0, "app")
from joblib import load
import snscrape.modules.twitter as sntwitter
from src.config import conf
from pymongo import MongoClient
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from src.utils.database import Database
import pandas as pd
from pathlib import Path

app = FastAPI()
tfidf, model = load('{}/{}'.format(Path(__file__).with_name('models'), 'lr.joblib'))


def scrape_account(account_name):
    '''
    return tweets from account_name
    '''
    max_tweets = 100
    tweets = []
    match = 'from:{}'.format(account_name)
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(match).get_items()):
        if i >= max_tweets:
            break
        tweets.append({
            "tweet_id": tweet.id,
            "account_name": account_name,
            "content": tweet.content
        })
    return tweets
    
 

def predict_tweet(tweet):
    prediction = list(model.predict_proba(tfidf.transform([tweet['content']]))[0])
    labels = ['droite', 'gauche']
    prediction_dict = {
        'position': labels[prediction.index(max(prediction))],
        labels[0]: prediction[0],
        labels[1]: prediction[1]
    }
    tweet = {**tweet, **prediction_dict}
    with Database() as db: 
        db.api.insert_one(tweet.copy())
    return tweet



@app.post("/predict")
async def predict(r: Request):
    form = await r.form()
    tweet = dict(form)
    tweet = predict_tweet(tweet)
    return tweet



@app.get("/predict/account/{account_name}")
def predict_account(account_name: str):
    with Database() as db:
        tweets = list(db.api.find({"account_name": account_name}, {"_id":0, "gauche":1, "droite":1}))
    if len(tweets) > 0:
        df = pd.DataFrame(tweets)
        return {
            'droite': df.droite.mean(),
            'gauche': df.gauche.mean(),
        }
    else:
        tweets = scrape_account(account_name)
        for tweet in tweets:
            predict_tweet(tweet)
        predict_account(account_name)


@app.get("/tweets/{account_name}")
def get_tweets(account_name: str):
    return scrape_account(account_name)


    

