import tweepy
from os import environ
from sys import stderr

try:
    consumer_key = environ['TWITTER_CONSUMER_KEY']
    consumer_secret = environ['TWITTER_CONSUMER_SECRET']
    access_key = environ['TWITTER_ACCESS_KEY']
    access_secret = environ['TWITTER_ACCESS_SECRET']


except KeyError as e:
    print('Error: The twitter credentials not set', file=stderr)
    exit(1)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
