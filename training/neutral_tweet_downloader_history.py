####################################################################
# The goal of this script is to download as much of the timeline as
# possible (3200 tweets) of each neutral twitter feed.
# This script is meant to be run once, in the beginning of the data
# mining phase.
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

## load the list of neutral twitter feed handles
f = open('../neutral_twitter_feeds.txt', 'r')
neutralfeedlist = []
for line in f:
  neutralfeedlist.append(line[0:len(line)-1])


## download the timelines
results = []
for i in range(len(neutralfeedlist)):
  print 'downloading timeline from @' + neutralfeedlist[i]
  j=0
  cond = True
  tmpresults = []
  while cond:
    if j == 0:
      tmpresults.append(twitter_api.statuses.user_timeline(screen_name = neutralfeedlist[i], count=200))
    else:
      tmpresults.append(twitter_api.statuses.user_timeline(screen_name = neutralfeedlist[i], count=200, max_id = maxid)) 
    maxid = tmpresults[j][-1]['id'] - 1
    if j == 15:
      cond = False
    j += 1
  tmpresults = [item for sublist in tmpresults for item in sublist] #flatten
  print 'tweets collected: ' + str(len(tmpresults))
  with open('../../tweet_data/training_data/neutral_tweet_data/neutral_data_timelinehistory_'+ neutralfeedlist[i], 'w') as outfile:
    json.dump(tmpresults, outfile)
  print 'pausing for 3 min' #pause to avoid going over Twitter's rate limit of 100 API calls/hour
  time.sleep(5*60)




