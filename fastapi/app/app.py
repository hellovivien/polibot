from fastapi import FastAPI
import sys
sys.path.insert(0, "app")
from joblib import load
import snscrape.modules.twitter as sntwitter
from config import conf
from pymongo import MongoClient
from datetime import datetime
import uvicorn

app = FastAPI()
tfidf, model = load('app/models/lr.joblib')
client = MongoClient(conf['mongo_uri'])
db = client.politweet


def build_tweet(tweet):
    tweet_dict = {}
    fields_to_keep = ['url','date','content','renderedContent','id','replyCount','retweetCount','likeCount','quoteCount','conversationId','lang','sourceLabel','hashtags','cashtags']
    fields_to_bool = ['retweetedTweet','quotedTweet','inReplyToTweetId','mentionedUsers']
    for field in fields_to_keep:
        if hasattr(tweet, field):
            tweet_dict[field] = getattr(tweet, field)
    for field in fields_to_bool:
        if hasattr(tweet, field):
            tweet_dict[field] = bool(getattr(tweet, field))
    return tweet_dict

def scrape_account(account_name, max_tweets=10):
    db.predictions.drop()
    tweets = []
    match = 'from:{}'.format(account_name)
    session = {'account_name': account_name}
    tweets = []
    total_gauche = 0
    total_droite = 0
    print(match)
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(match).get_items()):
        if max_tweets is not None and i > max_tweets:
            break
        print(tweet.user.username)
        prediction = predict(tweet.content)
        prediction['scrapping'] = build_tweet(tweet)
        total_gauche += prediction['gauche']
        total_droite += prediction['droite']
        tweets.append(prediction)
    num_of_tweets = len(tweets)
    if num_of_tweets > 0:
        score_gauche = total_gauche/num_of_tweets
        score_droite = total_droite/num_of_tweets
        if score_gauche>score_droite:
            position="gauche"
        elif score_droite>score_gauche:
            position="droite"
        else:
            position="égalité"
        session['num_of_tweets'] = num_of_tweets
        session['score_gauche'] = score_gauche
        session['score_droite'] = score_droite
        session['position'] = position
        res = session.copy()
        res['date'] = datetime.now()
        session['tweets'] = tweets
        db.predictions.insert_one(session)
    else:
        res = {'details':'no tweets'}
    return res
    
 

def predict(input):
    predictions = list(model.predict_proba(tfidf.transform([input]))[0])
    labels = ['droite', 'gauche']
    predictions = {
        'input': input,
        'position': labels[predictions.index(max(predictions))],
        labels[0]: predictions[0],
        labels[1]: predictions[1]
    }
    return predictions


@app.get("/predict/{input}")
def predict_input(input: str):
    return predict(input)

@app.get("/predict/account/{account_name}")
def predict_account(account_name: str):
    return scrape_account(account_name)

    

