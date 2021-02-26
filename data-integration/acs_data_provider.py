#!/usr/bin/env python

# Copyright © 2021 Yokesh Thirumoorthi
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pandas as pd

# Import acs census data
# nrows : int, default None
# nrows is the number of rows of file to read. Its useful for reading pieces of large files
df = pd.read_csv('data/acs2017_census_tract_data.csv', nrows=None)

# Renaming few column
df=df.rename(columns={
    'State':'state',
    'County':'county',
    'TotalPop': 'population',
    'Income':'income',
    'Poverty':'poverty'
    })

# Retain only the required columns and ignore the rest
df=pd.DataFrame(df, columns=['state', 'county', 'population', 'income', 'poverty'])

# Print the shape of df rows,columns
print(df.shape)

def compute_poverty_population(df):
    return (df.population * df.poverty) / 100

# Poverty is givan in % for each tract, which could not be summed up while using groupby. 
# So create a new column: Povery population = (population * povety_percent) / 100'
def get_poverty_transformed_df(df):
    poverty_transformed_df = pd.DataFrame(df)
    poverty_transformed_df['poverty_population'] = compute_poverty_population(df)
    return poverty_transformed_df

# Groupby County and State. 
# Get total for population, income and poverty_population
def get_acs_df(df):    
    aggDict = {'population':['sum'], 'income':['sum'], 'poverty_population':['sum']}
    columnNames = {'income': 'income', 'population': 'population', 'poverty_population': 'poverty_population'}
    acs_df = df.groupby(['county', 'state']) \
            .agg(aggDict) \
            .rename(columns=columnNames) \
            .reset_index() 
    
    #  Get rid of the count subtables inside agrregated columns
    acs_df.columns = acs_df.columns.droplevel(1)

    # Recalculate ipc for groiped data
    acs_df['income_per_capita'] = acs_df.income + acs_df.population
    # show povery as percentage
    acs_df['poverty'] = acs_df.poverty_population / acs_df.population
    # Povery population is no more required. Delete it.
    del df['poverty_population']

    return acs_df

def getDataFrame():
    poverty_transformed_df = get_poverty_transformed_df(df)
    acs_df = get_acs_df(poverty_transformed_df)

    return acs_df    
