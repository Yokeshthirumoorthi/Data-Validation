#!/usr/bin/env python
import pandas as pd

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 35)
pd.set_option('display.max_rows', 200)
# nrows : int, default None
# nrows is the number of rows of file to read. Its useful for reading pieces of large files
df = pd.read_csv('crashdata.csv', nrows=None)

# Print the shape of df rows,columns
print(df.shape)

# Renaming few columns of interest
df=df.rename(columns={
    'Crash ID':'crash_id',
    'Record Type':'record_type',
    'Vehicle ID':'vehicle_id',
    'Participant ID':'participant_id',
    'Crash Month':'crash_month',
    })

def numLen(num):
  return len(str(abs(num)))

def chk_only_valid_record_type_exists(df):
    return df.record_type.isin([1,2,3]).all()

def chk_only_valid_crash_id_exists(df):
    return (df.crash_id.apply(numLen) == 7).all()

def chk_crash_month_limit_validity(df):
    return df.crash_month.dropna().between(1,12).all()

# Assertion 1: Existence Assertion
# Assertion 1.a: All Records must have a record_type and the record_type should be either 1, 2 or 3
print(chk_only_valid_record_type_exists(df))

# Assertion 1.b: All record must have a crash_id and crash_id should be 8 digit long
print(chk_only_valid_crash_id_exists(df))

# Asssertion 2: Limit Assertion
# Assertion 2.a: Data in Crash month field should fall with in range 1 10 12.
print(chk_crash_month_limit_validity(df))

# # Seperate out crash data
# crash_data = df[df['record_type'] == 1] 
# # Seperate out vehicle data
# vehicle_data = df[df['record_type'] == 2]
# # Seperate out person data
# person_data = df[df['record_type'] == 3]
