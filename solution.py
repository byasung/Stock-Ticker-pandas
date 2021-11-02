#!/usr/bin/env python
# coding: utf-8

import numpy as np
import csv
import pandas as pd
header = ["Ticker","na1","bid","ask","trade","bidvol","askvol","tradevol","update","na2","date","sec_passed","openp","na3","condition","na4"]
table = pd.read_csv('scandi.csv',names=header)
#print ("Done reading csv")
with open('answer.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

answer = pd.DataFrame(columns = ['mean bid-ask', 'median bid-ask','mean trade','median trade','longest trade','mean tick change','median tick change','longest tick change'])

checknull = table['condition'].isnull()
checkXT = table['condition'] == 'XT'
#print("filter out unneccesary conditions")
table = table[checkXT | checknull] #only select the condition codes = XT and null
#print("Now sort ticker")
table = table.sort_values(by=['Ticker'])
table = table.set_index('Ticker')
#print("Now get bid-ask spread")
table['bid ask spread']=table['ask']-table['bid']
answer['median bid-ask']=table.groupby(['Ticker'])[["bid ask spread"]].median()['bid ask spread']
answer['mean bid-ask']=table.groupby(['Ticker'])[["bid ask spread"]].mean()['bid ask spread']

#mean and median time between trades
table2 = pd.DataFrame(table[table['update'] == 3])
#print("Now get trade time difference data")
table2.sort_values(['Ticker', 'sec_passed'], inplace=True)
table2['time diffs'] = table2.groupby('Ticker')['sec_passed'].diff()
answer['median trade']=table2.groupby(['Ticker'])[["time diffs"]].median()['time diffs']
answer['mean trade']=table2.groupby(['Ticker'])[["time diffs"]].mean()['time diffs']
answer['longest trade']=table2.groupby(['Ticker'])[["time diffs"]].max()['time diffs']

#print("now do tick change")
table3 = pd.DataFrame(table)

table3['ticker diff'] = table3.groupby('Ticker')['trade'].diff()
table3 =table3[table3['ticker diff']!=0]
table3.sort_values(['Ticker', 'sec_passed'], inplace=True)
table3['ticker time diffs'] = table3.groupby('Ticker')['sec_passed'].diff()

answer['median tick change']=table3.groupby(['Ticker'])[["ticker time diffs"]].median()['ticker time diffs']
answer['mean tick change']=table3.groupby(['Ticker'])[["ticker time diffs"]].mean()['ticker time diffs']
answer['longest tick change']=table3.groupby(['Ticker'])[["ticker time diffs"]].max()['ticker time diffs']

#print(answer)

answer.to_csv('/Users/tracysung/Downloads/italre/answer.csv',index=True,header=True)
