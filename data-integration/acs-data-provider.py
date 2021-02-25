#!/usr/bin/env python
import pandas as pd

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 200)

# nrows : int, default None
# nrows is the number of rows of file to read. Its useful for reading pieces of large files
df = pd.read_csv('data/acs2017_census_tract_data.csv', nrows=None)


# Renaming few columns of interest
df=df.rename(columns={
    'State':'state',
    'County':'county',
    'TotalPop': 'population',
    'Income':'income',
    'Poverty':'poverty'
    })

df=pd.DataFrame(df, columns=['state', 'county', 'population', 'income', 'poverty'])

# Print the shape of df rows,columns
print(df.shape)
df['poverty_count'] = df['population'] * df['poverty'] / 100

aggdict = {'population':['sum'], 'income':['sum'], 'poverty_count':['sum']}
columnNames = {'income': 'income', 'population': 'population', 'poverty_count': 'poverty_count'}
acsDf = df.groupby(['county', 'state']) \
        .agg(aggdict) \
        .rename(columns=columnNames) \
        .reset_index()

acsDf.columns = acsDf.columns.droplevel(1)
acsDf['income_per_capita'] = acsDf['income'] + acsDf['population']
acsDf['poverty'] = acsDf['poverty_count'] / acsDf['population']

counties_to_filter = [
    'Loudoun County', #Virginia
    'Washington County', #Oregon, 
    'Harlan County', #Kentucky,
    'Malheur County' #Oregon
]

states_to_filter = [
    'Virginia',
    'Oregon', 
    'Kentucky',
    'Oregon'
]

Filterdf = pd.DataFrame({
    'state': states_to_filter,
    'county': counties_to_filter
})

print(pd.merge(Filterdf, acsDf, how='left', on=['county', 'state']))