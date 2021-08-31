from fastapi.testclient import TestClient

import sys
from src.config import conf
from src.utils.database import Database
import urllib
import re
from main import app
test_client = TestClient(app)


def assert_predict(input, response):
    '''
    check status_code and response object
    '''
    json = response.json()
    assert response.status_code == 200
    assert json['content'] == input
    total = 0
    targets = ('droite', 'gauche')
    for target in targets:
        assert target in json
        assert type(json[target]) == float
        assert json[target] >= 0 and json[target] <= 1
        total += json[target]
    assert total > 0.99 and total < 1.01



def test_predict():
    '''
    we test ours predictions and api

    '''
    num_of_tweets_by_side = 50
    min_score = 0.75
    with Database() as db:
        left_tweets = db.tweets.find({'group': {'$in': conf['parties']['gauche']}}, {'content':1}).limit(num_of_tweets_by_side)
        right_tweets = db.tweets.find({'group': {'$in': conf['parties']['droite']}}, {'content':1}).limit(num_of_tweets_by_side)
    custom_inputs = {
        "gauche" : [
            "j'aime la gauche",
            "vive l'égalité et la solidarité entre les peuples"
        ],
        "droite" : [
            "j'aime la droite",
            "il faut réaffirmer notre souveraineté nationale"
        ]
    }
    db_inputs = {
        "gauche": left_tweets,
        "droite": right_tweets
    }
    # for each custom inputs prediction must be valid or test will fails
    for side, inputs in custom_inputs.items():
        for input in inputs:
            response = test_client.post("/predict", data = {"content":input})
            json = response.json()
            assert_predict(input, response)
            assert json['position'] == side

    # calculate valid score of our predictions with model data, score must be > 0.75 because our model has 0.85 score
    db_inputs_valid = 0
    for side, inputs in db_inputs.items():
        for input in inputs:
            input = input['content']
            response = test_client.post("/predict", data = {"content":input})
            json = response.json()
            assert_predict(input, response)
            if json['position'] == side:
                db_inputs_valid += 1
    score = db_inputs_valid/num_of_tweets_by_side
    assert(score > min_score)


def test_predict_account():
    '''
    same tests but for account
    '''
    accounts_gauche = ("JLMelenchon",)
    accounts_droite = ("MLP_officiel",)
    min_score = 0.75
    for account in accounts_gauche:  
        response = test_client.get("/predict/account/{}".format(account))
        print(response.json())
        assert response.status_code == 200
        json = response.json()
        total = 0
        targets = ('droite', 'gauche')
        for target in targets:
            assert target in json
            assert type(json[target]) == float
            assert json[target] >= 0 and json[target] <= 1
            total += json[target]
        assert total > 0.99 and total < 1.01                    



    ##
    # note for encoding and decoding a query parameter :
    # remove url : input = re.sub(r'http\S+', '', input['content'])
    # encode : input = urllib.parse.quote_plus(input)
    # decode : input = urllib.parse.unquote_plus(input)
    # i switch from get to post requests cause cant handle all parsing issues without adding lot of regex. e.g. (2/2)
    ##