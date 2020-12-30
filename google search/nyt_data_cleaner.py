#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 16:14:21 2020

@author: alfiantjandra
"""
import pandas as pd
import numpy as np

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



df_us = pd.read_csv("nyt_us.csv")
df = pd.read_csv("nyt_us_states.csv")

''' Taking dates subset '''
df['date'] = pd.to_datetime(df['date'])
mask = (df['date'] > '2020-09-29') & (df['date'] <= '2020-12-28')
df = df.loc[mask]

df_us['date'] = pd.to_datetime(df_us['date'])
mask_us = (df_us['date'] > '2020-09-29') & (df_us['date'] <= '2020-12-28')
df_us = df_us.loc[mask_us]



'''Convert to ISO'''
states = list(set(df['state']))
df['state'].replace(us_state_abbrev,inplace=True)
df = df.drop(columns = ['fips'])


df.to_csv("us_states.csv", index = False)
df_us.to_csv("us.csv",index=False)


