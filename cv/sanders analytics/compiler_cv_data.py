## import necessary libraries
import sys
import twitter
import json
import pandas as pd
import os

headers=['sentiment','created_at','id','lang','screen_name','retweet','text']
path = '../../../tweet_data/cv_data/sanders_analytics/'
file_list = [filename for filename in os.listdir(path + 'raw_data/')]

tweets=[]

## compile all the neutral tweets
j=0
for filename in file_list:
  with open(path + 'raw_data/' + filename) as json_data:
    data = json.load(json_data)
    RT = u'retweeted_status' in data.keys()
    tweets.append([ 'unknown', data['created_at'], data['id'], data['lang'], data['user']['screen_name'], RT, data['text']])
    print 'compiling: '+filename+', file '+str(j+1)+'/'+str(len(file_list))
    j=j+1

## save
df = pd.DataFrame(tweets, columns=headers)
df.to_pickle(path + 'sanders_analytics_cv_data_unprocessed.pkl')

