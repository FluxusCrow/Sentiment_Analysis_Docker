import tweepy
import time
from datetime import datetime
import logging
import random
import pymongo
import os

##################
# Authentication #
##################
BEARER_TOKEN = "<BEARER_TOKEN>"         # BEARER_TOKEN needs to be added to run this file     

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

########################
# Get User Information #
########################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

user = "rasbt"
response = client.get_user(
    username= user,
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
)

user = response.data

print(dict(user))


#########################
# Get a user's timeline #
#########################

# https://docs.tweepy.org/en/stable/pagination.html#tweepy.Paginator
# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

cursor = tweepy.Paginator(
    method=client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
).flatten(limit=20)

# Create a connection to the MongoDB database server
client_mongo = pymongo.MongoClient(host='mongodb') # hostname = servicename for docker-compose pipeline

# Create/use a database
db = client_mongo.twitter
# equivalent of CREATE DATABASE tweets;

# Define the collection
collections = db.tweets
# equivalent of CREATE TABLE tweet_data;

for tweet in cursor:
    print(tweet.text)
    logging.warning('-----Tweet being written into MongoDB-----')
    logging.warning(tweet)
    collections.insert_one(dict(tweet)) #equivalent of INSERT INTO tweet_data VALUES (....);
    logging.warning(str(datetime.now()))
    logging.warning('----------\n')

    time.sleep(3)


#####################
# Search for Tweets #
#####################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_recent_tweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

# - means NOT
search_query = "rasbt -is:retweet -is:reply -is:quote lang:de -has:links"

cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    query=search_query,
    tweet_fields=['author_id', 'created_at', 'public_metrics'],
).flatten(limit=20)

for tweet in cursor:
    print(tweet.text+'\n')


## Create a connection to the MongoDB database server
#client_mongo = pymongo.MongoClient(host='mongodb') # hostname = servicename for docker-compose pipeline
#
## Create/use a database
#db = client_mongo.twitter
## equivalent of CREATE DATABASE tweets;
#
## Define the collection
#collection = db.tweets
## equivalent of CREATE TABLE tweet_data;


#while True:
#    # What we actually want to do is to insert the tweet into MongoDB
#    tweet = {'username': user, 'text': tweet.text}
#    # Insert the tweet into the collection
#
#    logging.warning('-----Tweet being written into MongoDB-----')
#    logging.warning(tweet)
#    collection.insert_one(tweet) #equivalent of INSERT INTO tweet_data VALUES (....);
#    logging.warning(str(datetime.now()))
#    logging.warning('----------\n')
#
#    time.sleep(3)