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

def is_all_record_types_valid(df):
    return df.record_type.isin([1,2,3]).all()

def is_all_creash_id_valid(df):
    return (df.crash_id.apply(numLen) == 7).all()

def is_crash_month_limit_valid(df):
    return df.crash_month.dropna().between(1,12).all()

def validateData():
    # Assertion 1: Existence Assertion
    # Assertion 1.a: All Records must have a record_type and the record_type should be either 1, 2 or 3
    if not is_all_record_types_valid(df):
        raise ValueError("Existance Assertion Failed for record_type")

    # Assertion 1.b: All record must have a crash_id and crash_id should be 8 digit long
    if not is_all_creash_id_valid(df):
        raise ValueError("Existance Assertion Failed for crash_id")

    # Asssertion 2: Limit Assertion
    # Assertion 2.a: Data in Crash month field should fall with in range 1 10 12.
    if not (is_crash_month_limit_valid(df)):
        raise ValueError("Limit Assertion Failed for crash_month")

    print("All validations passed successfully")

# # Seperate out crash data
# crash_data = df[df['record_type'] == 1] 
# # Seperate out vehicle data
# vehicle_data = df[df['record_type'] == 2]
# # Seperate out person data
# person_data = df[df['record_type'] == 3]

validateData()