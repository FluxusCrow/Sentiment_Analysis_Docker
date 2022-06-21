# Sentiment analysis of Tweets - dockerized

## General info
Automated sentiment analysis of tweets of a Twitter user. The default user is "rasbt". The programm will get the latest tweets of the user, save them in a mongodb, analyze the sentiment of each tweet, save them in a postgresdb and finally post the tweet with the most negative and the tweet with the most positive sentiment to slack via a slackbot. Each of this processes is realized in a docker container.

## Technologies
* Python 3.9.7
* Docker 22.06.0-beta.0, build 3e9117b
* libraries and its versions are listed in requirements.txt and can be installed with:
```
$ conda install --name <environment_name> --file requirements.txt
```

## Setup
1. In the get_tweets.py file add your Twitter BEARER TOKEN:
```
12 BEARER_TOKEN = "<BEARER_TOKEN>"
```

2. In the same file you can change the Twitter user name (optional):
```
26 user = "rasbt"
```

3. In the slackbot.py file add your slack webhook_url:
```
10 webhook_url = "<webhook_url>"
```

4. To create all docker images, go to the directory containing the docker-compose.yml file and run in your terminal:
```
$ docker-compose build
```

5. Finall, to start all docker containers run in the terminal:
```
$ docker-compose up -d
```
