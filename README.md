# Start

## Streamlit

**online**: https://share.streamlit.io/hellovivien/polibot/main/streamlit/app/app.py

**local**:
```bash
cd streamlit/app
python start.py
```

## API (not ready yet)

**local**:
```bash
cd fastapi/app
python start.py
```

# Data

## Political parties

* **AGIR-E**: Agir ensemble
* **DEM**: Mouvement Démocrate (MoDem) et Démocrates apparentés
* **DLF**: Debout la France
* **EDS**: Écologie démocratie solidarité
* **FI**: La France insoumise
* **GDR**: Gauche démocrate et républicaine
* **GE**: Génération Écologie
* **LAREM**: La République en Marche
* **LDS**: Ligue du Sud
* **LND**: Les Nouveaux Démocrates
* **LR**: Les Républicains
* **LT**: Libertés et Territoires
* **RN**: Rassemblement National
* **SOC**: Socialistes et apparentés
* **UDI_I**: UDI et Indépendants

## Database fields

**accounts**:
* _id: MongoDB id
* id: twitter id
* sex
* first_name
* last_name
* group: partie politique abbrégé
* group_name: partie politique complet
* username: compte twitter
* facebook: compte facebook
* displayname: affichage nom sur twitter
* description
* rawDescription
* descriptionUrls
* verified
* created
* followersCount
* friendsCount
* statusesCount
* favouritesCount
* listedCount: nombres de listes crées
* mediaCount: nombre d'images

**tweets**:
* _id: MongoDB id
* id: twitter id
* account_id
* group: partie politique
* url
* date
* content
* renderedContent: contenu tel qu'il est affiché sur le site, les urls sont raccourcies, à voir s'il y a d'autres différences qui le rendrait plus propre que "content".
* replyCount
* retweetCount
* likeCount
* quoteCount
* conversationId
* lang
* sourceLabel: appareil de saisie (iphone, android...)
* retweetedTweet: si vrai c'est un retweet
* quotedTweet: si vrai il cite un autre tweet
* inReplyToTweetId: si vrai c'est en réponse à un autre tweet
* mentionedUsers: si vrai mentionne des gens dans le tweet
* hashtags
* cashtags


## Get Droite-Gauche from group

```py
# "AGIR-E": "centre-droit", # https://fr.wikipedia.org/wiki/Groupe_Agir_ensemble
# "DEM": "centre", # https://fr.wikipedia.org/wiki/Mouvement_d%C3%A9mocrate_(France)
# "DLF": "droite-plus", # https://fr.wikipedia.org/wiki/Debout_la_France
# "EDS": "centre-gauche", # https://fr.wikipedia.org/wiki/Groupe_%C3%89cologie_d%C3%A9mocratie_solidarit%C3%A9
# "FI": "gauche-plus", # https://fr.wikipedia.org/wiki/La_France_insoumise
# "GDR": "gauche-plus", # https://fr.wikipedia.org/wiki/Groupe_de_la_Gauche_d%C3%A9mocrate_et_r%C3%A9publicaine
# "GE": "centre-gauche", # https://fr.wikipedia.org/wiki/G%C3%A9n%C3%A9ration_%C3%A9cologie
# "LAREM": "centre", # https://fr.wikipedia.org/wiki/La_R%C3%A9publique_en_marche
# "LDS": "droite-plus", # https://fr.wikipedia.org/wiki/Ligue_du_Sud_(France)
# "LND": "gauche", # https://fr.wikipedia.org/wiki/Les_Nouveaux_D%C3%A9mocrates
# "LR": "droite", # https://fr.wikipedia.org/wiki/Les_R%C3%A9publicains
# "LT": "centre", # https://fr.wikipedia.org/wiki/Groupe_Libert%C3%A9s_et_territoires
# "RN": "droite-plus", # https://fr.wikipedia.org/wiki/Rassemblement_national
# "SOC": "gauche", # https://fr.wikipedia.org/wiki/Groupe_socialiste_(Assembl%C3%A9e_nationale)
# "UDI_I": "centre-droit", # https://fr.wikipedia.org/wiki/Union_des_d%C3%A9mocrates_et_ind%C3%A9pendants

def get_target(group):
    '''
    Takes the political group as an argument
    Returns 'droite' or 'gauche'
    Else returns 'centre' e.g. if it is a group of the center
    '''
    target_dict = {
      "droite":["AGIR-E", "DLF", "LDS", "LR", "RN", "UDI_I"],
      "gauche":["EDS", "FI", "GDR", "GE", "LND", "SOC"],
    }
    if group in target_dict["droite"]:
      return "droite"
    elif group in target_dict["gauche"]:
      return "gauche"
    else:
      return "centre"
```

# MongoDB usage

database connection
```py
uri = "mongodb+srv://politweet:<password>@cluster0.0rn9i.mongodb.net/politweet?retryWrites=true&w=majority" # replace <password>
client = MongoClient(uri)
db = client.politweet
```

get all tweets with all fields
```py
cursor = db.tweets.find() #cursor
tweets = list(db.tweets.find()) #fetchall
```

get all tweets except retweeted and quoted ones, filter the result to only get content and group fields
```py
tweets = list(db.tweets.find({"retweetedTweet":False, "quotedTweet":False}, {"_id":0, "content":1, "group":1}))
```

convert to a dataframe:
```py
df = pd.DataFrame(tweets) # you can use cursor instead too
```

save to json and load as a dataframe
```py
with open('data.json', 'w') as f:
    json.dump(jsonable_encoder(tweets), f)
df = pd.read_json('data.json')
```

join with account collection to get extra fields, here we add followersCount field: 
```py
pipeline = [{'$lookup': 
                {'from' : 'accounts',
                 'localField' : 'account_id',
                 'foreignField' : '_id',
                 'as' : 'account'}},
            {'$unwind': '$account'},
            {'$project': {'_id':0, 'content':1, 'followersCount': '$account.followersCount'}}]
cursor = db.tweets.aggregate(pipeline)
```