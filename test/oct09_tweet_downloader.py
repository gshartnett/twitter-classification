####################################################################
# the goal of this script is to download tweets associated with the 
# Oct. 09 2016 Presidential Debate
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

#later on in processing, delete tweets that cannot be classified as pos or neg

tweets=[]
search_results1 = twitter_api.search.tweets(q='#debates', count=100, lang='en')
search_results2 = twitter_api.search.tweets(q='#debates2016', count=100, lang='en')
search_results3 = twitter_api.search.tweets(q='#debatenight', count=100, lang='en')
statuses1 = search_results1['statuses']
statuses2 = search_results2['statuses']
statuses3 = search_results3['statuses']
tweets.append(statuses1)
tweets.append(statuses2)
tweets.append(statuses3)
tweets = [item for sublist in tweets for item in sublist]

today = str(datetime.utcnow())
date_year = today[0:4]
date_month = today[5:7]
date_day = today[8:10]
date_hour = today[11:13]
date_min = today[14:16]

date = date_year + '_' + date_month + '_' + date_day + '_' + date_hour + '_' + date_min

with open('../../tweet_data/test_data/debate_data/oct09_data_'+ date, 'w') as outfile:
    json.dump(tweets, outfile)



