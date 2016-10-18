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

headers=['sentiment','event date','created_at','id','lang','screen_name','retweet','text']

## filename lists
path = '../../tweet_data/test_data/debate_data/'
sept26_file_list = [filename for filename in os.listdir(path) if filename.startswith('sept26_data_2016')]
oct09_file_list = [filename for filename in os.listdir(path) if filename.startswith('oct09_data_2016')]

## tweet compiler function
def compile(file_list, name):
  table = []
  j=0
  for filename in file_list:
    with open(path + filename) as json_data:
      print 'compiling: '+filename+', file '+str(j+1)+'/'+str(len(sept26_file_list))
      data = json.load(json_data)
      for i in range(len(data)):
        RT = u'retweeted_status' in data[i].keys()
        table.append([ 'unknown', name, data[i]['created_at'], data[i]['id'], data[i]['lang'], data[i]['user']['screen_name'], RT, data[i]['text']])
      j=j+1
  return table

table_sept26 = compile(sept26_file_list, 'sept26')
table_oct09 = compile(oct09_file_list, 'oct09')

print 'total number of Sept. 26 tweets:', len(table_sept26)
print 'total number of Oct. 9 tweets:', len(table_oct09)

## "pickle" the data after converting it to a dataframe
df = pd.DataFrame(table_sept26 + table_oct09, columns=headers)
df.to_pickle(path + 'debate_data_unprocessed.pkl')


