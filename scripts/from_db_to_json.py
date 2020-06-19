import pandas as pd
import sqlite3
import csv
import tweepy
from scripts.authentication import consumer_key, consumer_secret, access_key, access_secret, auth, api
import time
import json


CONSUMER_KEY = consumer_key
CONSUMER_SECRET= consumer_secret
OAUTH_TOKEN = access_key
OAUTH_TOKEN_SECRET = access_secret

conn = sqlite3.connect('Twitter.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT distinct tweet_id FROM election_tweets", conn)
db_df.to_csv('database.csv', index=False)



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

with open('database.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

data.remove(data[0])

results=[]

print("downloading the tweets")
for d in data:
	if data.index(d)%700==0 and data.index(d)>0:
		print("next packet")
		time.sleep(60*15)
	try:
		tweet=api.get_status(d[0], tweet_mode='extended')
		results.append(tweet)
	except:
		print(data.index(d))
        
    
print(type(results[0]))

with open('./twitterdb.json', 'w') as fout:
   json.dump(results , fout)