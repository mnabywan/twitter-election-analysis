import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
from matplotlib.pyplot import figure
import numpy as np

from datetime import date, timedelta


def candidate_sum(table, date, candidate,  conn):

    hash_pop = ("SELECT  sum(favorite_count) as favorites, count(*) as count, sum(retweet_count) as retweets "
                "FROM {} WHERE candidate_name = \'{}\' AND created_at LIKE \'{}\'".format(table, candidate, date))
    df = pd.read_sql_query(hash_pop, conn)
    return df


conn = sqlite3.connect('../db/Twitter.db')
cur = conn.cursor()


sdate = date(2020, 3, 30)   # start date
edate = date(2020, 5, 15)   # end date

delta = edate - sdate       # as timedelta


duda_tweets = {'Day': [],
               'Count': [],
               'Favorite count': [],
               'Retweet count': []}

kidawa_tweets = { 'Day': [],
               'Count': [],
               'Favorite count': [],
               'Retweet count': []}

bosak_tweets = {'Day': [],
                'Count': [],
               'Favorite count': [],
               'Retweet count': []}

biedron_tweets = { 'Day': [],
               'Count': [],
               'Favorite count': [],
               'Retweet count': []}

kosiniak_tweets = { 'Day': [],
               'Count': [],
               'Favorite count': [],
               'Retweet count': []}

holownia_tweets = {'Day': [],
                'Count': [],
               'Favorite count': [],
               'Retweet count': []}

candidates = {
    "Duda": duda_tweets,
    "Biedron": biedron_tweets,
    "Bosak": bosak_tweets,
    "Holownia": holownia_tweets,
    "Kidawa": kidawa_tweets,
    "Kosiniak": kosiniak_tweets
}



days_list = []

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    day = str(day)
    days_list.append(day)

for candidate in candidates.keys():
    for day in days_list:
        df = candidate_sum('candidates_tweets',  day + ' %', candidate, conn )
        candidates.get(candidate).get('Day').append(day)
        candidates.get(candidate).get('Count').append(df['count'])
        candidates.get(candidate).get('Retweet count').append(df['retweets'])
        candidates.get(candidate).get('Favorite count').append(df['favorites'])


dates = [pd.to_datetime(d) for d in days_list]

outfile = "../server/static/charts/favourite_count.svg"
for item in candidates.keys():
    fav_list = candidates.get(item)['Favorite count']
    count_list = candidates.get(item)['Count']
    retweet_list = candidates.get(item)['Retweet count']
    plt.scatter(dates, fav_list, s =5, )
    plt.xlabel("Date")
    plt.ylabel("Favorite count")
    plt.title("Favorite count for date for accounts connected to each candidate ")
    plt.plot(dates, fav_list, label=item, )


plt.legend(loc=2) #upper left
fig = plt.gcf()
fig.set_size_inches(10, 5)
plt.savefig(fname=outfile)
plt.show()
plt.close()


outfile =  "../server/static/charts/tweets_count.svg"

for item in candidates.keys():
    fav_list = candidates.get(item)['Favorite count']
    count_list = candidates.get(item)['Count']
    retweet_list = candidates.get(item)['Retweet count']

    plt.scatter(dates, count_list, s =5, )
    plt.xlabel("Date")
    plt.ylabel("Number of tweets")
    plt.title("Number of tweets for date for accounts connected to each candidate ")
    plt.plot(dates, count_list, label=item )

plt.legend(loc=2)
fig = plt.gcf()
fig.set_size_inches(10, 5)
plt.savefig(fname=outfile, )
plt.show()
plt.close()

outfile = "../server/static/charts/retweet_count.svg"

for item in candidates.keys():
    fav_list = candidates.get(item)['Favorite count']
    count_list = candidates.get(item)['Count']
    retweet_list = candidates.get(item)['Retweet count']

    plt.scatter(dates, retweet_list, s =5, )
    plt.xlabel("Date")
    plt.ylabel("Retweet count")
    plt.title("Retweet count for date for accounts connected to each candidate ")
    plt.plot(dates, retweet_list, label=item,)


plt.legend(loc=2)
fig = plt.gcf()
fig.set_size_inches(10, 5)
# plt.figure(figsize=(8,4))
plt.savefig(fname=outfile)
plt.show()
plt.close()

print("{: >20} {: >20} {: >20} {: >20} {: >20} {: >20}".format("Candidate", "Avg tweets/day", "Avg favorites/day ", "Avg retweets/day", "Avg favorites/tweet", "Avg retweets/tweet"))

for c in candidates.keys():
    df = pd.DataFrame(candidates.get(c))
    count_mean = int((df['Count']).mean())
    favorite_mean = int((df['Favorite count']).mean())
    retweet_mean = int((df['Retweet count']).mean())
    favorite_per_tweet = int (favorite_mean/count_mean)
    rt_per_tweet = int(retweet_mean/count_mean)

    print("{: >20} {: >20} {: >20} {: >20} {: >20} {: >20}".format(c, count_mean, favorite_mean, retweet_mean, favorite_per_tweet, rt_per_tweet))




