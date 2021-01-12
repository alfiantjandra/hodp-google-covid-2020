# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:34:22 2021

@author: alfian
"""

from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import pycountry
import time
import matplotlib.pyplot as plt


pytrend = TrendReq(hl='en-GB', tz=360)
colnames = ["keywords"]

""" list of keywords  """

words = ["covid symptoms", "loss of smell", "coronavirus vaccine", "covid testing"]


''' area code'''
list_subdivision = ['US-MA-506']


''' Scrape data and format into a single dataset; output: final_result '''
# final_result = pd.DataFrame()
# for x in range(0,len(words)):
#     dataset = []
#     for state in list_subdivision:
          
#           keywords = [words[x]]
#           pytrend.build_payload(
#           kw_list=keywords,
#           cat=0,
#           timeframe='2020-09-30 2020-12-28',
#           geo=state)
#           data = pytrend.interest_over_time()

#           if not data.empty:
              
#               data = data.drop(labels=['isPartial'],axis='columns')
#               data.columns = [words[x]]
#               dataset.append(data)
#           time.sleep(2)
          
#     result = pd.concat(dataset,axis =1)
#     result = result.div(100)
#     final_result = pd.concat([final_result,result],axis=1)
#     word = words[x]

# final_result.to_csv("boston trend.csv")    
          
df = pd.read_csv("boston covid data.csv")
df['date'] = pd.to_datetime(df['Date'])
mask = (df['date'] > '2020-09-29') & (df['date'] <= '2020-12-11')
df = df.loc[mask]
df.set_index('date',inplace=True)
df = df.drop(columns = ['Date'])

df_trends = pd.read_csv("boston trend.csv")
mask = (df_trends['date'] > '2020-09-29') & (df_trends['date'] <= '2020-12-11')
df_trends = df_trends.loc[mask]
df_trends['date']=pd.to_datetime(df_trends['date'])
df_trends.set_index('date',inplace=True)
print(df_trends)
print(df)
df = pd.concat([df,df_trends],axis=1)

def df_shifted(df, target=None, lag=0):
    if not lag and not target:
        return df
    new = {}
    for c in df.columns:
        if c == target:
            new[c] = df[target]
        else:
            new[c] = df[c].shift(periods=lag)
    return pd.DataFrame(data=new)


keywords = ["covid symptoms", "loss of smell", "coronavirus vaccine", "covid testing"]
MAX_DAY = 14

for word in keywords:
    points = []
    for i in range(2* MAX_DAY + 1):  # positive i means RSV from i days earlier is compared with current cases
        new_df = df_shifted(df, 'new cases', lag=i)
        points.append(new_df.corr().loc['new cases', word])
    
    plt.figure(figsize=(10,5))
    plt.plot(np.arange(2* MAX_DAY + 1), points, color='r',label=word)  
    plt.ylabel("Correlation", size=16)
    plt.xlabel("Shift", size=16)
    plt.xticks(np.arange(0, 29, 7))
    plt.title(f"{word.title()}",size=16)
    plt.show()

