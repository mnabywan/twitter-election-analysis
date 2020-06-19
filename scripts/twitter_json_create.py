import pandas as pd
import sqlite3
import csv
import tweepy
from authentication import consumer_key, consumer_secret, access_key, access_secret, auth, api
import time
import json 

CONSUMER_KEY = ""
CONSUMER_SECRET= ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

conn = sqlite3.connect('../db/Twitter.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT distinct tweet_id FROM candidates_tweets", conn)
db_df.to_csv('candidates.csv', index=False)



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

with open('new_tweets.csv', newline='') as f:
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

with open('./new_tweets.json', 'w') as fout:
   json.dump(results , fout)