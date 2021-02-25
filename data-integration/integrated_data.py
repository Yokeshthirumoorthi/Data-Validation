#!/usr/bin/env python
import pandas as pd
import acs_data_provider as acs
import covid_county_data_provider as covid

acsData = acs.getDataFrame()
covidData = covid.getDataFrame()

USADataFrame = pd.merge(acsData, covidData, how='left', on=['state', 'county'])

oregonDataFrame = USADataFrame.loc[USADataFrame['state'].isin(['Oregon'])]

print(oregonDataFrame)

oregonDataFrame['total_cases_normalized'] = (oregonDataFrame['total_cases'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['total_cases_normalized'].corr(oregonDataFrame['poverty']))

oregonDataFrame['total_deaths_normalized'] = (oregonDataFrame['total_deaths'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['total_deaths_normalized'].corr(oregonDataFrame['poverty']))


oregonDataFrame['total_cases_normalized'] = (oregonDataFrame['total_cases'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['total_cases_normalized'].corr(oregonDataFrame['income_per_capita']))

oregonDataFrame['total_deaths_normalized'] = (oregonDataFrame['total_deaths'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['total_deaths_normalized'].corr(oregonDataFrame['income_per_capita']))


oregonDataFrame['dec_cases_normalized'] = (oregonDataFrame['dec_cases'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['dec_cases_normalized'].corr(oregonDataFrame['poverty']))

oregonDataFrame['dec_deaths_normalized'] = (oregonDataFrame['dec_deaths'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['dec_deaths_normalized'].corr(oregonDataFrame['poverty']))


oregonDataFrame['dec_cases_normalized'] = (oregonDataFrame['dec_cases'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['dec_cases_normalized'].corr(oregonDataFrame['income_per_capita']))

oregonDataFrame['dec_deaths_normalized'] = (oregonDataFrame['dec_deaths'] * 100000) / oregonDataFrame['population'] 
print(oregonDataFrame['dec_deaths_normalized'].corr(oregonDataFrame['income_per_capita']))

print(oregonDataFrame)

# 


USADataFrame['total_cases_normalized'] = (USADataFrame['total_cases'] * 100000) / USADataFrame['population'] 
print(USADataFrame['total_cases_normalized'].corr(USADataFrame['poverty']))

USADataFrame['total_deaths_normalized'] = (USADataFrame['total_deaths'] * 100000) / USADataFrame['population'] 
print(USADataFrame['total_deaths_normalized'].corr(USADataFrame['poverty']))


USADataFrame['total_cases_normalized'] = (USADataFrame['total_cases'] * 100000) / USADataFrame['population'] 
print(USADataFrame['total_cases_normalized'].corr(USADataFrame['income_per_capita']))

USADataFrame['total_deaths_normalized'] = (USADataFrame['total_deaths'] * 100000) / USADataFrame['population'] 
print(USADataFrame['total_deaths_normalized'].corr(USADataFrame['income_per_capita']))


USADataFrame['dec_cases_normalized'] = (USADataFrame['dec_cases'] * 100000) / USADataFrame['population'] 
print(USADataFrame['dec_cases_normalized'].corr(USADataFrame['poverty']))

USADataFrame['dec_deaths_normalized'] = (USADataFrame['dec_deaths'] * 100000) / USADataFrame['population'] 
print(USADataFrame['dec_deaths_normalized'].corr(USADataFrame['poverty']))


USADataFrame['dec_cases_normalized'] = (USADataFrame['dec_cases'] * 100000) / USADataFrame['population'] 
print(USADataFrame['dec_cases_normalized'].corr(USADataFrame['income_per_capita']))

USADataFrame['dec_deaths_normalized'] = (USADataFrame['dec_deaths'] * 100000) / USADataFrame['population'] 
print(USADataFrame['dec_deaths_normalized'].corr(USADataFrame['income_per_capita']))

print(USADataFrame)