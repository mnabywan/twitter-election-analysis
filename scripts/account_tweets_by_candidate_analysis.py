import pandas as pd
import matplotlib.pyplot as plt
from candidates import DUDA_ACCOUNTS, KIDAWA_ACCOUNTS, BIEDRON_ACCOUNTS, KOSINIAK_ACCOUNTS, BOSAK_ACCOUNTS, HOLOWNIA_ACCOUNTS
from datetime import datetime
import sqlite3
from matplotlib.pyplot import figure
import numpy as np

from datetime import date, timedelta


conn = sqlite3.connect('../db/Twitter.db')
cur = conn.cursor()



def candidate_sum(table, date, candidate,  conn):
    hash_pop = ("SELECT  sum(favorite_count) as favorites, count(*) as count, sum(retweet_count) as retweets, author_name "
                "FROM {} WHERE candidate_name = \'{}\' AND created_at LIKE \'{}\' GROUP BY author_name ; ".format(table, candidate, date))
    df = pd.read_sql_query(hash_pop, conn)
    return df


def prepare_dict_for_candidate():
    duda_tweets ={}
    kidawa_tweets = {}
    holownia_tweets = {}
    kosianiak_tweets = {}
    bosak_tweets = {}
    biedron_tweets = {}


    for i in range(0, len(DUDA_ACCOUNTS)):
        duda_tweets[DUDA_ACCOUNTS[i]] = {
                    'Author' : [],
                    'Day': [],
                    'Count': [],
                    'Favorite count': [],
                    'Retweet count': []}

    for i in range(0, len(KIDAWA_ACCOUNTS)):
        kidawa_tweets[KIDAWA_ACCOUNTS[i]] = {
                    'Author' : [],
                    'Day': [],
                    'Count': [],
                    'Favorite count': [],
                    'Retweet count': []}

    for i in range(0, len(KOSINIAK_ACCOUNTS)):
        kosianiak_tweets[KOSINIAK_ACCOUNTS[i]] = {
                    'Author' : [],
                    'Day': [],
                    'Count': [],
                    'Favorite count': [],
                    'Retweet count': []}

    for i in range(0, len(BIEDRON_ACCOUNTS)):
        biedron_tweets[BIEDRON_ACCOUNTS[i]] = {
                    'Author' : [],
                    'Day': [],
                    'Count': [],
                    'Favorite count': [],
                    'Retweet count': []}

    for i in range(0, len(BOSAK_ACCOUNTS)):
        bosak_tweets[BOSAK_ACCOUNTS[i]] = {
                    'Author' : [],
                    'Day': [],
                    'Count': [],
                    'Favorite count': [],
                    'Retweet count': []}

    for i in range(0, len(HOLOWNIA_ACCOUNTS)):
        holownia_tweets[HOLOWNIA_ACCOUNTS[i]] = {
                    'Author' : [],
                    'Day': [],
                    'Count': [],
                    'Favorite count': [],
                    'Retweet count': []}

    return duda_tweets, kidawa_tweets, kosianiak_tweets, biedron_tweets, holownia_tweets, bosak_tweets


def get_chart_for_candidate(candidate, candidate_dict, sdate, edate, delta, candidate_accounts):
    days_list = []

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        day = str(day)
        days_list.append(day)
    
    #Prepare data for each account connected to candidate
    for day in days_list:
        df = candidate_sum('candidates_tweets',  day + ' %', candidate, conn )
        for ac in candidate_accounts:
            if ac not in df.author_name.tolist():
                account = candidates.get(candidate)[ac]
                account.get('Author').append(ac)
                account.get('Day').append(day)
                account.get('Count').append(0)
                account.get('Retweet count').append(0)
                account.get('Favorite count').append(0)

        for index, row in df.iterrows():
            candidate_acc = candidates.get(candidate)[row['author_name']]
            candidate_acc.get('Author').append(row['author_name'])
            candidate_acc.get('Day').append(day)
            candidate_acc.get('Count').append(row['count'])
            candidate_acc.get('Retweet count').append(row['retweets'])
            candidate_acc.get('Favorite count').append(row['favorites'])


    dates = [pd.to_datetime(d) for d in days_list]


    print("{: >20} {: >20} {: >20} {: >20} {: >20} {: >20}".format("Account", "Avg tweets/day", "Avg favorites/day ", "Avg retweets/day", "Avg favorites/tweet", "Avg retweets/tweet"))

    for c in candidate_dict.keys():
        df = pd.DataFrame(candidate_dict.get(c))
        #
        count_mean = round(float((df['Count']).mean()), 1)
        favorite_mean = int((df['Favorite count']).mean())
        retweet_mean = int((df['Retweet count']).mean())
        if count_mean == 0:
            favorite_per_tweet = 0
            rt_per_tweet = 0
        else:
            favorite_per_tweet = int (favorite_mean/count_mean)
            rt_per_tweet = int(retweet_mean / count_mean)

        #
        print("{: >20} {: >20} {: >20} {: >20} {: >20} {: >20}".format(c, count_mean, favorite_mean, retweet_mean, favorite_per_tweet, rt_per_tweet))
    print("\n")



if __name__ == '__main__':
    
    duda_tweets, kidawa_tweets, kosiniak_tweets,\
        biedron_tweets, holownia_tweets, bosak_tweets = prepare_dict_for_candidate()

    candidates = {
        "Duda": duda_tweets,
        "Biedron": biedron_tweets,
        "Bosak": bosak_tweets,
        "Holownia": holownia_tweets,
        "Kidawa": kidawa_tweets,
        "Kosiniak": kosiniak_tweets
    }


    sdate = date(2020, 3, 30)   # start date
    edate = date(2020, 5, 15)   # end date

    delta = edate - sdate       # as timedelta


    for c in candidates.keys():
        if c == "Duda":
            get_chart_for_candidate(c, candidates.get(c), sdate, edate, delta, DUDA_ACCOUNTS)
        elif c == "Kidawa":
            get_chart_for_candidate(c, candidates.get(c), sdate, edate, delta, KIDAWA_ACCOUNTS)
        elif c == "Bosak":
            get_chart_for_candidate(c, candidates.get(c), sdate, edate, delta, BOSAK_ACCOUNTS)
        elif c == "Biedron":
            get_chart_for_candidate(c, candidates.get(c), sdate, edate, delta, BIEDRON_ACCOUNTS)
        elif c == "Kosiniak":
            get_chart_for_candidate(c, candidates.get(c), sdate, edate, delta, KOSINIAK_ACCOUNTS)
        elif c == "Holownia":
            get_chart_for_candidate(c, candidates.get(c), sdate, edate, delta, HOLOWNIA_ACCOUNTS)
