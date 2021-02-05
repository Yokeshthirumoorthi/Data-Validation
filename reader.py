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
    'Participant ID':'participant_id'
    })

def numLen(num):
  return len(str(abs(num)))

# Assertion 1: Existence Assertion
# Assertion 1.a: All Records must have a record_type and the record_type should be either 1, 2 or 3
record_type = df.record_type
(record_type>3).any() # any record_type has value greater than 3
(record_type<1).any() # any record_type has value lesser than 1

# Assertion 1.b: All record must have a crash_id and crash_id should be 8 digit long
crash_id = df.crash_id
(crash_id).isnull()
(crash_id.apply(numLen) != 7).any()
# (len(str(crash_id)) == 8).all()


# Asssertion 2: Limit Assertion
# Assertion 2.a: 


# # Seperate out crash data
# crash_data = df[df['record_type'] == 1] 
# # Seperate out vehicle data
# vehicle_data = df[df['record_type'] == 2]
# # Seperate out person data
# person_data = df[df['record_type'] == 3]
