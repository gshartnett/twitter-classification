####################################################################
# The goal of this script is to download the previous days' tweets
# tweets from the set of neutral twitter feeds.
# This script is meant to run once a day.
####################################################################


## import necessary libraries
import sys
import twitter
import json
from datetime import datetime, timedelta
import os

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


## create a time variable for yesterday's date (in UTC time), format is [year, month, day]
today = datetime.utcnow()
yesterday = today + timedelta(days=-1)
todayvec = [int(str(today)[0:4]), int(str(today)[5:7]), int(str(today)[8:10])]
yesterdayvec = [int(str(yesterday)[0:4]), int(str(yesterday)[5:7]), int(str(yesterday)[8:10])]

print 'today (in vector notation): ' + str(todayvec)
print 'yesterday (in vector notation): ' + str(yesterdayvec)

## if yesterday's tweets were already downloaded, don't bother running
f = open("../../tweet_data/training_data/neutral_tweet_data/neutral_log.txt", 'r')
daysdownloaded = []
for line in f:
  daysdownloaded.append(line[0:line.index(']')+1])
if str(yesterdayvec) in daysdownloaded:
  print 'aborting, already gathered yesterday\'s tweets'
  sys.exit(0)
    

## download tweets, starting with the most recent and stopping when 2-day old tweets are reached
results = []
for i in range(len(neutralfeedlist)):
  print 'downloading tweets from @' + neutralfeedlist[i]
  j=0
  cond = True
  tmpresults = []
  while cond:
    if j == 0:
      tmpresults.append(twitter_api.statuses.user_timeline(screen_name = neutralfeedlist[i], count=200))
    else:
      tmpresults.append(twitter_api.statuses.user_timeline(screen_name = neutralfeedlist[i], count=200, max_id = maxid)) 
    maxid = tmpresults[j][-1]['id'] - 1
    if tweetdate(tmpresults[j][-1]) != todayvec and tweetdate(tmpresults[j][-1]) != yesterdayvec:
      cond = False
    j += 1
  tmpresults = [item for sublist in tmpresults for item in sublist] #flatten
  tmpresults = [x for x in tmpresults if not tweetdate(x) != yesterdayvec] #throw out the tweets that weren't born yesterday
  results.append(tmpresults) #append to the main list
results = [item for sublist in results for item in sublist] #flatten
print '\ntotal number of tweets collected: ' + str(len(results))


with open('../../tweet_data/training_data/neutral_tweet_data/neutral_data_' + str(yesterday)[0:4] + '_' + str(yesterday)[5:7] + '_' + str(yesterday)[8:10], 'w') as outfile:
    json.dump(results, outfile)


## finish up by adding to the log file
f = open("../../tweet_data/training_data/neutral_tweet_data/neutral_log.txt", 'a')
f.write(str(yesterdayvec)+' '+str(len(results))+'\n')





