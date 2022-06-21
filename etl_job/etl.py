import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

time.sleep(10)  # seconds

# Select the database you want to use withing the MongoDB server
db = client.twitter

pg = create_engine('postgresql://docker_user:1234@postgresdb:5432/twitter', echo=True)
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')

analyzer = SentimentIntensityAnalyzer()

mentions_regex= '@[A-Za-z0-9_]+'
url_regex='https?:\/\/\S+' #this will not catch all possible URLs
hashtag_regex= '#'
rt_regex= 'RT\s'

def clean_tweets(tweet):
    tweet = re.sub(mentions_regex, '', tweet)  #removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet) #removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet) #removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet) #removes most URLs
    text = tweet
    return tweet


docs = db.tweets.find()
for doc in docs:
    text = doc['text']
    text=clean_tweets(text)
    score = analyzer.polarity_scores(text)["compound"]
    #score = 1.0  # placeholder value
    query = "INSERT INTO tweets VALUES (%s, %s);"
    pg.execute(query, (text, score))
