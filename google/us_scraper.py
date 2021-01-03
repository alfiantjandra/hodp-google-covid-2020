#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 14:05:25 2020

@author: alfiantjandra
"""
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import time

pytrend = TrendReq(hl='en-GB', tz=360)
colnames = ["keywords"]

""" list of keywords ( max. 5) """
df2 = ['loss of taste']


""" Area to be scraped """
list_subdivision = ['US']

'''Scrape data and format into one dataset; output: final_result'''
for y in list_subdivision:
    dataset = []
    for x in range(0,len(df2)):
          keywords = [df2[x]]
          pytrend.build_payload(
          kw_list=keywords,
          cat=0,
          timeframe='2020-09-30 2020-12-28',
          geo=y)
          data = pytrend.interest_over_time()
          if not data.empty:
              data = data.drop(labels=['isPartial'],axis='columns')
              dataset.append(data)
    

    result = pd.concat(dataset, axis=1)
    if list_subdivision.index(y) == 0:
        final_result = result
    else:
        final_result = pd.concat([final_result,result],axis=1)
    time.sleep(1)


final_result = final_result.div(100)
final_result.to_csv("../US_google_trends/loss of taste.csv")
              

