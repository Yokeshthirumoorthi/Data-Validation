#!/usr/bin/env python
import pandas as pd
import acs_data_provider as acs
import covid_county_data_provider as covid

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 200)

def filter_for_selected_counties(df):
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

    filter_df = pd.DataFrame({
        'state': states_to_filter,
        'county': counties_to_filter
    })
    
    result_df = pd.merge(filter_df, df, how='left', on=['county', 'state'])

    return result_df

def get_corrs(dataframe):
    df = dataframe.copy()
    df['total_cases_normalized'] = (df.total_cases * 100000) / df.population
    corrs_cases_poverty = df.total_cases_normalized.corr(df.poverty)
    corrs_cases_ipc = df.total_cases_normalized.corr(df.income_per_capita)

    df['total_deaths_normalized'] = (df.total_deaths * 100000) / df.population
    corrs_deaths_poverty = df.total_deaths_normalized.corr(df.poverty)
    corrs_deaths_ipc = df.total_deaths_normalized.corr(df.income_per_capita)

    df['dec_cases_normalized'] = (df.dec_cases * 100000) / df.population
    corrs_dec_cases_poverty = df.dec_cases_normalized.corr(df.poverty)
    corrs_dec_cases_ipc = df.dec_cases_normalized.corr(df.income_per_capita)

    df['dec_deaths_normalized'] = (df.dec_deaths * 100000) / df.population
    corrs_dec_deaths_poverty = df.dec_deaths_normalized.corr(df.poverty)
    corrs_dec_deaths_ipc = df.dec_deaths_normalized.corr(df.income_per_capita)

    corrs_df = pd.DataFrame({
        'corrs_cases_poverty': [corrs_cases_poverty],
        'corrs_cases_ipc': [corrs_cases_ipc],
        'corrs_deaths_poverty': [corrs_deaths_poverty],
        'corrs_deaths_ipc': [corrs_deaths_ipc],
        'corrs_dec_cases_poverty':[corrs_dec_cases_poverty],
        'corrs_dec_cases_ipc':[corrs_dec_cases_ipc],
        'corrs_dec_deaths_poverty':[corrs_dec_deaths_poverty],
        'corrs_dec_deaths_ipc':[corrs_dec_deaths_ipc]
    })

    return corrs_df
    
def print_results():
    acs_df = acs.getDataFrame()
    covid_df = covid.getDataFrame()

    USA_df = pd.merge(acs_df, covid_df, how='left', on=['state', 'county'])
    Oregon_df = USA_df[USA_df.state.isin(['Oregon'])]

    acs_selected_counties_subset_df = filter_for_selected_counties(acs_df)
    covid_selected_counties_subset_df = filter_for_selected_counties(covid_df)

    corrs_usa_df = get_corrs(USA_df)
    corrs_oregon_df = get_corrs(Oregon_df)

    print(acs_selected_counties_subset_df)
    print(covid_selected_counties_subset_df)
    print(Oregon_df)
    print(corrs_usa_df)
    print(corrs_oregon_df)

print_results()