import tweepy
import datetime, time
import sqlite3

from candidates import *
from authentication import consumer_key, consumer_secret, access_key, access_secret, auth, api


conn = sqlite3.connect('../db/Twitter.db')
c = conn.cursor()

def select_all_tasks():
    cur = conn.cursor()
    cur.execute("SELECT tweet_id FROM duda_hashtags ")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def update_tweets_data(table_name):
    select_str = "SELECT tweet_id FROM {} WHERE retweet_count IS NULL".format(table_name)
    print(select_str)
    cur = conn.cursor()
    cur.execute(select_str)

    tweets = cur.fetchall()
    print(tweets)
    for row in tweets:
        print(row[0])
        tweet_id = row[0]
        try:
            tweet = api.get_status(tweet_id)
            created_at = str(tweet.created_at)
            retweet_count = tweet.retweet_count
            favorite_count = tweet.favorite_count
            author_name = tweet.author.screen_name
            str1 = "UPDATE \"{}\"  SET favorite_count = {}, created_at = \"{}\", retweet_count= {}, author_name = \"{}\" " \
                   " WHERE tweet_id = \"{}\"".format(table_name, favorite_count,
                                                     created_at, retweet_count, author_name, tweet_id)
            print(str)
            cur.execute(str1)
            conn.commit()
        except tweepy.error.TweepError:
            pass





def get_tweets_by_hashtag(api, hashtag, table_name, date_until=None, date_since=None):
    print(hashtag)
    for tweet in tweepy.Cursor(api.search,
                               q= hashtag,
                                since = date_since,
                                until = date_until,
                                rpp=10,
                                count= 10
                               ).items():
        if 'RT @' not in tweet.text:
            id = tweet.id
            is_tweet_in_base = "SELECT tweet_id from {} where tweet_id = {}".format(table_name, id)
            #print(is_tweet_in_base)
            c.execute(is_tweet_in_base)
            id_in_base = c.fetchall()
            if not id_in_base:
                created_at = str(tweet.created_at)
                retweet_count = tweet.retweet_count
                favorite_count = tweet.favorite_count
                author_name = tweet.author.screen_name
                print(tweet.created_at)
                str1 = "INSERT INTO {}(tweet_id, hashtag, created_at, retweet_count, favorite_count, author_name) VALUES ({}, \"{}\", \"{}\", {}, {}, \"{}\" )"
                str1 = str1.format(table_name, id, hashtag, created_at, retweet_count, favorite_count, author_name)
                print(str)
                c.execute(str1)
                conn.commit()


def get_tweets_by_user(api, username, candidate):
    page = 1
    end = False

    while True:
        tweets = api.user_timeline(username, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days  <= 31:
                if 'RT @' not in tweet.text:
                    ''' Handle unique  '''
                    id = tweet.id
                    is_tweet_in_base = "SELECT tweet_id from candidates_tweets where tweet_id = {}".format(id)
                    c.execute(is_tweet_in_base)
                    id_in_base = c.fetchall()
                    if not id_in_base:
                        created_at = str(tweet.created_at)
                        retweet_count = tweet.retweet_count
                        favorite_count = tweet.favorite_count
                        author_name = tweet.author.screen_name
                        print(tweet.created_at)
                        str1 = "INSERT INTO candidates_tweets(tweet_id, candidate_name, author_name, favorite_count, retweet_count ,created_at) " \
                               "VALUES ({}, \"{}\", \"{}\", {}, {}, \"{}\")"
                        str1 = str1.format(id, candidate, author_name, favorite_count, retweet_count, created_at)
                        print(str1)
                        c.execute(str1)
                        conn.commit()
            else:
                end = True
                return

        if not end:
             page = page + 1
             time.sleep(10)


def get_tweets_by_journalist_account(api, table_name, journalist):
    print(table_name)
    print(journalist)
    page = 1
    end = False

    while True:
        tweets = api.user_timeline(journalist, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days  <= 31:
                if 'RT @' not in tweet.text and any(word in tweet.text for word in ELECTION_KEYWORDS):
                    ''' Handle unique  '''
                    id = tweet.id
                    is_tweet_in_base = "SELECT tweet_id from journalist_tweets where tweet_id = {}".format(id)
                    c.execute(is_tweet_in_base)
                    id_in_base = c.fetchall()
                    if not id_in_base:
                        created_at = str(tweet.created_at)
                        retweet_count = tweet.retweet_count
                        favorite_count = tweet.favorite_count
                        author_name = tweet.author.screen_name
                        print(tweet.created_at)
                        str1 = "INSERT INTO journalist_tweets(tweet_id, author_name, favorite_count, retweet_count ,created_at) " \
                               "VALUES ({}, \"{}\", {}, {}, \"{}\")"
                        str1 = str1.format(id, author_name, favorite_count, retweet_count, created_at)
                        c.execute(str1)
                        conn.commit()
            else:
                end = True
                return

        if not end:
             page = page + 1
            #time.sleep(10)


def get_tweets_by_candidates_accounts():
# DUDA_ACCOUNTS + KIDAWA_ACCOUNTS + KOSINIAK_ACCOUNTS\
#                     + BIEDRON_ACCOUNTS +HOLOWNIA_ACCOUNTS +
    accounts_list =BOSAK_ACCOUNTS
    for user in accounts_list:
        if user in DUDA_ACCOUNTS:
            candidate = DUDA
        elif user in KIDAWA_ACCOUNTS:
            candidate = KIDAWA
        elif user in KOSINIAK_ACCOUNTS:
            candidate = KOSINIAK
        elif user in BIEDRON_ACCOUNTS:
            candidate = BIEDRON
        elif user in BOSAK_ACCOUNTS:
            candidate = BOSAK
        elif user in HOLOWNIA_ACCOUNTS:
            candidate = HOLOWNIA

        get_tweets_by_user(api, user, candidate)


def get_tweets_by_hashtag_start():
    table_name = "election_tweets"
    for hashtag in ELECTION_HASHTAGS:
        get_tweets_by_hashtag(api, hashtag, table_name=table_name, date_since="2020-05-07")


def get_tweets_by_candidates_hashtags_start():

#DUDA_HASHTAGS  KIDAWA_HASHTAGS + KOSINIAK_HASHTAGS + \
              #  BIEDRON_HASHTAGS + HOLOWNIA_HASHTAGS +
    hashtag_list = BOSAK_HASHTAGS

    for hashtag in hashtag_list:
        if hashtag in DUDA_HASHTAGS:
            table_name = "duda_hashtags"
        elif hashtag in KIDAWA_HASHTAGS:
            table_name = "kidawa_hashtags"
        elif hashtag in KOSINIAK_HASHTAGS:
            table_name = "kosiniak_hashtags"
        elif hashtag in BIEDRON_HASHTAGS:
            table_name = "biedron_hashtags"
        elif hashtag in HOLOWNIA_HASHTAGS:
            table_name = "holownia_hashtags"
        elif hashtag in BOSAK_HASHTAGS:
            table_name = "bosak_hashtags"
        get_tweets_by_hashtag(api, hashtag, table_name=table_name,  date_since="2020-05-07")

def get_tweets_by_journalists_account_start():
    table_name = "journalist_tweets"
    for journalist in JOURNALISTS_ACCOUNTS:
        get_tweets_by_journalist_account(api, table_name, journalist)


def insert_accounts_data(table):
    accounts_list = DUDA_ACCOUNTS + KIDAWA_ACCOUNTS + KOSINIAK_ACCOUNTS \
                     + BIEDRON_ACCOUNTS + HOLOWNIA_ACCOUNTS + BOSAK_ACCOUNTS
    for account in JOURNALISTS_ACCOUNTS:
        user = api.get_user(account)
        created_at = str(user.created_at)
        followers_count = user.followers_count
        statuses_count = user.statuses_count
        favourites_count = user.favourites_count
        friends_count = user.friends_count
        str1 = "INSERT INTO \"{}\"(account, created_at, followers_count, statuses_count, favourites_count, friends_count)" \
               " VALUES (\"{}\", \"{}\", {}, {}, {}, {})"
        str1 = str1.format(table, account, created_at, followers_count, statuses_count, favourites_count, friends_count)
        print(str1)
        c.execute(str1)
        conn.commit()


if __name__ == '__main__':

    get_tweets_by_candidates_accounts()
    #insert_accounts_data(table="journalist_accounts")
    #get_tweets_by_journalists_account_start()
    #update_tweets_data("journalist_tweets")
    #get_tweets_by_hashtag_start()
    #get_tweets_by_candidates_hashtags_start()
    #get_tweets_by_candidates_accounts()
    # update_tweets_data("candidates_tweets")
    # update_tweets_data("election_tweets")
    # tweet = api.get_status(1256274433473470465)
    # print(tweet.text)
    # # print(tweet.text)