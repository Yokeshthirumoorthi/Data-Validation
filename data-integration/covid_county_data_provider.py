#!/usr/bin/env python

# Copyright © 2021 Yokesh Thirumoorthi
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pandas as pd

# Import covid data
# nrows : int, default None
# nrows is the number of rows of file to read. Its useful for reading pieces of large files
df = pd.read_csv('data/COVID_county_data.csv', nrows=None)

# Tranform values in county column to match values in acs table.
# Doing this helps in joining dataframes. 
df['county'] = df['county'] + ' County';

# Print the shape of df rows,columns
print(df.shape)

# Aggregate data by county and state
def get_aggreated_df(df, newColumnNames):
    aggDict = {'cases':['sum'], 'deaths':['sum']}
    aggreated_df = df.groupby(['county', 'state']) \
                    .agg(aggDict) \
                    .rename(columns=newColumnNames) \
                    .reset_index()
    #  Get rid of the count subtables inside agrregated columns
    aggreated_df.columns = aggreated_df.columns.droplevel(1)                    
    return aggreated_df
    
# Subset with values only in dec
def get_dec_df(df):
    DEC_START = '2020-12-01'
    DEC_END = '2020-12-30'
    return df.loc[df['date'].isin([DEC_START,DEC_END])]

# Build a single dataframe that has all the required columns
def getDataFrame():
    total_cases_df = get_aggreated_df(df, newColumnNames={'cases': 'total_cases', 'deaths': 'total_deaths'})
    dec_cases_df = get_aggreated_df(df, newColumnNames={'cases': 'dec_cases', 'deaths': 'dec_deaths'})
    final_df = pd.merge(total_cases_df, dec_cases_df, how='left', on=['county', 'state'])
    return final_df    
