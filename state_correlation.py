#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 17:52:46 2021

@author: alfiantjandra
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry



df= pd.read_csv("google/us_states_cases.csv", index_col = "date")
outlying_area = ['US-PR','US-GU','US-AS','US-MP','US-VI','US-UM','US-AK']
df = df.drop(["AK","PR","GU","MP","VI"], axis =1)
us_states = list(df.columns)
df.index = pd.to_datetime(df.index)
df.columns = [state + " cases" for state in df.columns]



keywords = ["loss of taste", "covid symptoms", "loss of smell", "face mask", "coronavirus vaccine", "covid testing"]
final_result = pd.DataFrame()
data = []
column = ['keyword']
column.extend(us_states)
for word in keywords:
    
    df_state = pd.read_csv(f"google/state {word}.csv", index_col = "date")
    df_state.index = pd.to_datetime(df_state.index)
    result = []
    for state in us_states:
        temp_df = pd.concat([df[state+" cases"],df_state[state]], axis=1)
        temp_result = temp_df.corr()[state][state+" cases"]
        result.append(temp_result)
    result.insert(0,word)
    data.append(result)

final_result = pd.DataFrame(np.array(data), columns = column )
final_result.to_csv("state_correlation.csv")

            
    
    
    



