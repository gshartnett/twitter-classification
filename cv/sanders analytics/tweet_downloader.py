## import necessary libraries
import sys
import twitter
import json
import time
from datetime import datetime, timedelta
import pandas as pd


## initialize the twitter api
execfile("../../../twitter_OAUTH_credentials.py") #load the OAUTH credentials (stored in a separate file for privacy reasons
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)


## load the list of tweets
corpus = pd.read_csv('corpus.csv')
corpus.columns = ['query','sentiment','id']


## download the tweets
for i in range(len(corpus)):
  try:
    x = twitter_api.statuses.show(_id=corpus['id'].iloc[i], _method='GET')
    print 'downloaded tweet: ' + str(i+1) + '/' + str(len(corpus)+1)
    with open('raw_data/data_'+ str(x['id']), 'w') as outfile:
      json.dump(x, outfile)
    print x['text']
    ## pause to prevent violating rate limits 
    time.sleep(10) #in seconds
  except:
    print 'skipped tweet: ' + str(i+1) + '/' + str(len(corpus)+1)
