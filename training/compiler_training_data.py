####################################################################
# The goal of this script is take the downloaded tweets, which are
# stored as lists of json elements in many different files, and to 
# compile them into one single CSV file.
####################################################################

## import necessary libraries
import os
import sys
import json
import csv
import pandas as pd

headers=['sentiment','created_at','id','lang','screen_name','retweet','text']
path = '../../tweet_data/training_data/'
neutral_file_list = [filename for filename in os.listdir(path + 'neutral_tweet_data') if filename.startswith('neutral_data')]
pos_file_list = [filename for filename in os.listdir(path + 'pm_tweet_data') if filename.startswith('pos_data')]
neg_file_list = [filename for filename in os.listdir(path + 'pm_tweet_data') if filename.startswith('neg_data')]
table=[]

## compile all the neutral tweets
j=0
for filename in neutral_file_list:
  with open(path + 'neutral_tweet_data/'+filename) as json_data:
    data = json.load(json_data)
    for i in range(len(data)):
      RT = u'retweeted_status' in data[i].keys()
      table.append([ 0, data[i]['created_at'], data[i]['id'], data[i]['lang'], data[i]['user']['screen_name'], RT, data[i]['text']])
    print 'compiling: '+filename+', file '+str(j+1)+'/'+str(len(neutral_file_list))
    j=j+1

## compile all the postive tweets
j=0
for filename in pos_file_list:
  with open(path + 'pm_tweet_data/' + filename) as json_data:
    data = json.load(json_data)
    for i in range(len(data)):
      RT = u'retweeted_status' in data[i].keys()
      table.append([ 1, data[i]['created_at'], data[i]['id'], data[i]['lang'], data[i]['user']['screen_name'], RT, data[i]['text']])
    print 'compiling: '+filename+', file '+str(j+1)+'/'+str(len(pos_file_list))
    j=j+1

## compile all the negative tweets
j=0
for filename in neg_file_list:
  with open(path + 'pm_tweet_data/' + filename) as json_data:
    data = json.load(json_data)
    for i in range(len(data)):
      RT = u'retweeted_status' in data[i].keys()
      table.append([ -1, data[i]['created_at'], data[i]['id'], data[i]['lang'], data[i]['user']['screen_name'], RT, data[i]['text']])
    print 'compiling: '+filename+', file '+str(j+1)+'/'+str(len(neg_file_list))
    j=j+1

print 'total number of tweets:', len(table)

## "pickle" the data after converting it to a dataframe
df = pd.DataFrame(table, columns=headers)
df.to_pickle(path + 'training_data_unprocessed.pkl')


