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
    'Serial #':'serial_no',
    'County Code':'county_code',
    'Crash Month':'crash_month',
    'Crash Day':'crash_day',
    'Crash Year':'crash_year',
    'Week Day Code': 'week_day_code',
    'Latitude Degrees': 'latitude_degrees'
    })

CRASH_RECORD_ID = 1
VEHICLE_RECORD_ID = 2
PERSON_RECORD_ID = 3
CRASH_ID_LENGTH = 7
JAN = 1
DEC = 12
SUNDAY = 0
SATURDAY = 7

def numLen(num):
  return len(str(abs(num)))

def is_all_record_types_valid(df):
    return df.record_type.isin([CRASH_RECORD_ID,VEHICLE_RECORD_ID,PERSON_RECORD_ID]).all()

def is_all_creash_id_valid(df):
    return (df.crash_id.isnull()).sum() == 0

def is_crash_month_limit_valid(df):
    return df.crash_month.dropna().between(JAN,DEC).all()

def is_lat_degree_valid(df):
    return df.latitude_degrees.dropna().between(41,47).all()

def is_week_day_code_limit_valid(df):
    return df.week_day_code.dropna().between(SUNDAY,SATURDAY).all()

def is_all_participant_id_unique(df):
    return df.participant_id.dropna().is_unique

def is_all_serial_county_year_combination_unique(df):
    crash_df=df[df['record_type'] == 1] 
    serial_no=crash_df['serial_no'].astype(str)
    county_code=crash_df['county_code'].astype(str)
    crash_year=crash_df['crash_year'].astype(str)
    return (serial_no + county_code + crash_year).is_unique

def is_all_participant_id_has_crash_id(id):
    comparable_columns = ['crash_id','participant_id']
    # set up crash_participant_data frame
    crash_participant_df = df[comparable_columns]
    # remove rows with almost all missing data
    crash_participant_df = crash_participant_df.dropna(axis = 1, how ='all', thresh=2)
    # check if there is any null in crash id
    return crash_participant_df.crash_id.isnull().sum() == 0

def validateData():
    # Assertion 1: Existence Assertion
    # Assertion 1.a: All Records must have a record_type and the record_type should be either 1, 2 or 3
    if not is_all_record_types_valid(df):
        raise ValueError("Existance Assertion Failed for record_type")

    # Assertion 1.b: All record must have a crash_id
    if not is_all_creash_id_valid(df):
        raise ValueError("Existance Assertion Failed for crash_id")

    # Assertion 2: Limit Assertion
    # Assertion 2.a: Data in Crash month field should fall with in range 1 t0 12.
    if not (is_crash_month_limit_valid(df)):
        raise ValueError("Limit Assertion Failed for crash_month")

    # Assertion 2.b: Data in Week Day Code field should fall with in range 1 t0 7.
    if not (is_week_day_code_limit_valid(df)):
        raise ValueError("Limit Assertion Failed for week_day_code")

    # Assertion 2.c: When entered, Latitude Degrees must be a whole number between 41 and 47, inclusive
    if not (is_lat_degree_valid(df)):
        raise ValueError("Limit Assertion Failed for latitude degree")

    # Assertion 3: Intra Record Check Assertion
    # Assertion 3a: Total Count of Persons Involved = Total Pedestrian Count + Total Pedalcyclist Count + Total Unknown Count + Total Occupant Count.
    # TODO

    # Assertion 3b: Total Un-Injured Persons Count = total number of persons involved - the number of personsinjured - the number of persons killed
    # TODO
    
    # Assertion 4: Inter Record Check Assertion
    # Assertion 4a: Total crash should not vary more than 50% month on mpnth
    # TODO

    # Assertion 4b: Latitude Minutes must be null when Latitude Degrees is null
    # And Latitude Seconds must be null when Latitude Degrees is null
    # TODO

    # Distance from Intersection must = 0 when Road Character = 1
    # And Distance from Intersection must be > 0 when Road Character is not 1

    # Assertion 5: Summary Assertion
    # Assertion 5a: Check if all participant has unique id
    if not (is_all_participant_id_unique(df)):
        raise ValueError("Summary Assertion Failed for unique participant id")

    # Assertion 5b: Combination of Serial number + County + Year is unique
    if not (is_all_serial_county_year_combination_unique(df)):
        raise ValueError("Summary Assertion Failed for unique Serial number + County + Year combination")

    # Assertion 6: Referential Integrity Assertion
    # Assertion 6a: Each participant id has a crash id
    if not is_all_participant_id_has_crash_id(df):
        raise ValueError("Referential integrity Assertion Failed for participant_id:crash_id")

    # Assertion 6b: Every crash has a known lat long location
    # TODO

    # Assertion 7: Statistical Distribution Assertion
    # Assertion 7a: TODO
    # Assertion 7b: TODO

    print("All validations passed successfully")

validateData()