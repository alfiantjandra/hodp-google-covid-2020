#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:05:25 2020

@author: alfiantjandra
"""
from pytrends.request import TrendReq
import pandas as pd
import pycountry
import time
import matplotlib.pyplot as plt
import numpy as np
startTime = time.time()
pytrend = TrendReq(hl='en-GB', tz=360)


colnames = ["keywords"]
df2 = ['coronavirus','short breath','covid-19']

""" Conditioning covid dataset"""
covid =pd.read_csv("all-states-history.csv")
covid['date']=covid['date'].astype('datetime64[ns]')
covid = covid[['date','positive','positiveIncrease','negative','negativeIncrease','state']]


xd = list(pycountry.subdivisions.get(country_code='US'))
list_subdivision = []
for i in range(len(xd)):
    list_subdivision.append(xd[i].code)

outlying_area = ['US-PR','US-GU','US-AS','US-MP','US-VI','US-UM']
for x in outlying_area:
    list_subdivision.remove(x)

list1=list_subdivision[0:2]
list2= list_subdivision[44:51]

for y in list_subdivision:
    dataset = []
    for x in range(0,len(df2)):
          keywords = [df2[x]]
          pytrend.build_payload(
          kw_list=keywords,
          cat=0,
          timeframe='2020-02-01 2020-12-18',
          geo=y)
          data = pytrend.interest_over_time()
          if not data.empty:
              data = data.drop(labels=['isPartial'],axis='columns')
              dataset.append(data)
    

    result = pd.concat(dataset, axis=1)
    result = result.assign(state =y[3]+y[4])    
    if list_subdivision.index(y) == 0:
        result1 = result
    else:
        result1 = result1.append(result)
    time.sleep(2)


final_result = result1.merge(covid,on = ["date","state"])   
        
  
final_result.to_csv("dataset.csv")

plt.plot(final_result['coronavirus'])
plt.show()
              


# executionTime = (time.time() - startTime)
# print('Execution time in sec.: ' + str(executionTime))
