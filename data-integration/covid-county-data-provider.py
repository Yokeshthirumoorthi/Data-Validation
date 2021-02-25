#!/usr/bin/env python
import pandas as pd

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 200)

# nrows : int, default None
# nrows is the number of rows of file to read. Its useful for reading pieces of large files
df = pd.read_csv('data/COVID_county_data.csv', nrows=None)

# Print the shape of df rows,columns
print(df.shape)

# add count
aggdict = {'cases':['sum'], 'deaths':['sum']}
totalCases = df.groupby(['county', 'state']).agg(aggdict).rename(columns={'cases': 'total_cases', 'deaths': 'total_deaths'}).reset_index()

totalCases.columns = totalCases.columns.droplevel(1)

DEC_START = '2020-12-01'
DEC_END = '2020-12-30'
decDataFrame = df.loc[df['date'].isin([DEC_START,DEC_END])]
decCases = decDataFrame.groupby(['county', 'state']).agg(aggdict).rename(columns={'cases': 'dec_cases', 'deaths': 'dec_deaths'}).reset_index()
decCases.columns = decCases.columns.droplevel(1)

joinedDf = pd.merge(totalCases, decCases, how='left', on=['county', 'state'])
print(joinedDf)