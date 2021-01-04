#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 16:14:21 2020

@author: alfiantjandra
"""
import pandas as pd
import numpy as np
import os

''' Converter Dictionary '''
us_state_abbrev = {
'Alabama': 'AL',
'Alaska': 'AK',
'American Samoa': 'AS',
'Arizona': 'AZ',
'Arkansas': 'AR',
'California': 'CA',
'Colorado': 'CO',
'Connecticut': 'CT',
'Delaware': 'DE',
'District of Columbia': 'DC',
'Florida': 'FL',
'Georgia': 'GA',
'Guam': 'GU',
'Hawaii': 'HI',
'Idaho': 'ID',
'Illinois': 'IL',
'Indiana': 'IN',
'Iowa': 'IA',
'Kansas': 'KS',
'Kentucky': 'KY',
'Louisiana': 'LA',
'Maine': 'ME',
'Maryland': 'MD',
'Massachusetts': 'MA',
'Michigan': 'MI',
'Minnesota': 'MN',
'Mississippi': 'MS',
'Missouri': 'MO',
'Montana': 'MT',
'Nebraska': 'NE',
'Nevada': 'NV',
'New Hampshire': 'NH',
'New Jersey': 'NJ',
'New Mexico': 'NM',
'New York': 'NY',
'North Carolina': 'NC',
'North Dakota': 'ND',
'Northern Mariana Islands':'MP',
'Ohio': 'OH',
'Oklahoma': 'OK',
'Oregon': 'OR',
'Pennsylvania': 'PA',
'Puerto Rico': 'PR',
'Rhode Island': 'RI',
'South Carolina': 'SC',
'South Dakota': 'SD',
'Tennessee': 'TN',
'Texas': 'TX',
'Utah': 'UT',
'Vermont': 'VT',
'Virgin Islands': 'VI',
'Virginia': 'VA',
'Washington': 'WA',
'West Virginia': 'WV',
'Wisconsin': 'WI',
'Wyoming': 'WY'
}

us_state_values = list(us_state_abbrev.values())
us_state_values.remove('AS')


df = pd.read_csv("../covid_data/us_states_total.csv")
df_us = pd.read_csv("../covid_data/us_total.csv")

''' Taking dates subset '''
df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] >= '2020-09-29') & (df['date'] <= '2020-12-28')
df = df.loc[mask]

df_us['date'] = pd.to_datetime(df_us['date'])
mask_us = (df_us['date'] >= '2020-09-29') & (df_us['date'] <= '2020-12-28')
df_us = df_us.loc[mask_us]



'''Convert to ISO'''
states = list(set(df['state']))
df['state'].replace(us_state_abbrev,inplace=True)
df = df.drop(columns = ['fips'])



new_df = pd.DataFrame()
for state in us_state_values:
        temp_df = df[df['state'] == state]
        temp_df.index = pd.to_datetime(temp_df['date'])
    

        
        
        '''Convert into increase, remove top row'''
        temp_df['increase'] = temp_df["cases"].diff()
        temp_df = temp_df.drop(pd.to_datetime('2020-09-29'))
        
        temp_df = temp_df.drop(columns= ['cases','date','state','deaths'])
        temp_df = temp_df.rename(columns = {"increase": state})
        
        new_df = pd.concat([new_df,temp_df],axis=1)

new_df = new_df.reset_index()



df_us['increase'] = df_us["cases"].diff()
df_us = df_us[df_us['date'] != '2020-09-29']
df_us = df_us.drop(columns = ["cases","deaths"])



new_df.to_csv("us_states_cases.csv", index = False)
df_us.to_csv("us_cases.csv",index=False)


