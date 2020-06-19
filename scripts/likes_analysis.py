import pandas as pd
from pandas import DataFrame
import sqlite3
import matplotlib.pyplot as plt
from time import sleep
from os import environ

def candidate_sum(table, conn):
    
    hash_pop=("""SELECT '"""+table[0]+"""' as "candidate", sum(favorite_count) as favourites,sum(retweet_count) as retweets 
                                  FROM """+table[1])

    df = pd.read_sql_query(hash_pop, conn)
    return df

def save_likes_and_rts(conn, candidates, outfile='server/static/charts/likes_and_rts.svg'):
    dfl=[]
    for k in candidates.items():
        o=candidate_sum(k, conn)
        dfl.append(o)

    df = pd.concat(dfl)
    df.sort_values(by=['favourites'], inplace=True, ascending=False)
    df.reset_index()
    print(df)

    df.plot(x="candidate", y=["favourites", "retweets"], kind="bar")
    plt.tight_layout()
    plt.savefig(outfile)

def candidate_tweets(conn):
    hash_pop=("""SELECT candidate_name,count(tweet_id) as tweets_number FROM candidates_tweets  GROUP BY candidate_name ORDER BY count(tweet_id) desc limit 6""")

    df = pd.read_sql_query(hash_pop, conn)
    return df


def save_candidate_tweets(conn, candidates, outfile='server/static/charts/candidate_tweets.svg'):
    df2 = candidate_tweets(conn)

    df2.plot(x="candidate_name", y="tweets_number", kind="bar")
    plt.tight_layout()
    plt.savefig(outfile)

def authenticate():
    from authentication import api
    return api

def save_candidate_followers_and_friends(outfile1='server/static/charts/followers.svg', outfile2='server/static/charts/friends.svg'):
    diction=[]
    twitter = authenticate()
    for c in ['AndrzejDuda', 'M_K_Blonska', 'RobertBiedron', 'KosiniakKamysz', 'krzysztofbosak', 'szymon_holownia']:
        tweet = twitter.get_user(c)
        user={'candidate':c,"follower_count":tweet._json['followers_count'],"friends_count":tweet._json['friends_count']}
        diction.append(user)

    df5=pd.DataFrame(diction)
    df5.sort_values(by=['follower_count'], inplace=True, ascending=False)
    df5.plot(x="candidate", y=["follower_count"], kind="bar")
    plt.tight_layout()
    plt.savefig(outfile1)

    df5.sort_values(by=['friends_count'], inplace=True, ascending=False)
    df5.plot(x="candidate", y=["friends_count"], kind="bar")
    plt.tight_layout()
    plt.savefig(outfile2)

if __name__ == '__main__':
    conn = sqlite3.connect('db/Twitter.db')
    cur = conn.cursor() 
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=[]
    for name in res:
        tables.append(name[0])

    #TODO: fetch this from candidates file
    candidates={
        "Duda":'duda_hashtags',
        "Biedron":'biedron_hashtags',
        "Bosak":'bosak_hashtags',
        "Holownia":'holownia_hashtags',
        "Kidawa":'kidawa_hashtags',
        "Kosiniak":'kosiniak_hashtags'
    }
    save_likes_and_rts(conn, candidates)
    save_candidate_tweets(conn, candidates)
    save_candidate_followers_and_friends()
