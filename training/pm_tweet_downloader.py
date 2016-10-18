####################################################################
# the goal of this script is to download recent tweets with positive
# and negative emoticons
####################################################################


## import necessary libraries
import sys
import twitter
import json
import time
from datetime import datetime, timedelta


## return the UTC date of a tweet, in format [year,month,day]
def tweetdate(tweet):
  factors = []
  tempdate = tweet['created_at']
  monthlist = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  date = [int(tempdate[26:30]), monthlist.index(tempdate[4:7]) + 1, int(tempdate[8:10])]
  return date


## initialize the twitter api
execfile("../../twitter_OAUTH_credentials.py") #load the OAUTH credentials (stored in a separate file for privacy reasons
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

pos_emoticons = [':)']
neg_emoticons = [':(']
#later on in processing, delete tweets that cannot be classified as pos or neg

pos_tweets=[]
neg_tweets=[]
for i in range(len(pos_emoticons)):
  pos_search_results = twitter_api.search.tweets(q=pos_emoticons[i], count=100, lang='en')
  neg_search_results = twitter_api.search.tweets(q=neg_emoticons[i], count=100, lang='en')
  pos_statuses = pos_search_results['statuses']
  neg_statuses = neg_search_results['statuses']
  pos_tweets.append(pos_statuses)
  neg_tweets.append(neg_statuses)

pos_tweets = [item for sublist in pos_tweets for item in sublist]
neg_tweets = [item for sublist in neg_tweets for item in sublist]

today = str(datetime.utcnow())
date_year = today[0:4]
date_month = today[5:7]
date_day = today[8:10]
date_hour = today[11:13]
date_min = today[14:16]

date = date_year + '_' + date_month + '_' + date_day + '_' + date_hour + '_' + date_min

with open('../../tweet_data/training_data/pm_tweet_data/pos_data_'+ date, 'w') as outfile:
    json.dump(pos_tweets, outfile)
with open('../../tweet_data/training_data/pm_tweet_data/neg_data_'+ date, 'w') as outfile:
    json.dump(neg_tweets, outfile)


