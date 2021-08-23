from googletrans import Translator


def remove_duplicate_tweets(db):
    tweets = db.tweets.find()
    for tweet in tweets:
        duplicate = list(db.tweets.find({'id':tweet['id']}))
        if len(duplicate)>1:
            for duplicate in duplicate[1:]:
                db.tweets.delete_one(duplicate)
                print("{} has been deleted".format(duplicate['id']))

def translate(input):
    try:
        translater = Translator() 
        res = translater.translate(input, src='fr', dest='en')
        return res.text
    except:
        return None                