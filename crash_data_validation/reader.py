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
    'Crash Hour':'crash_hour',
    'Week Day Code': 'week_day_code',
    'Latitude Seconds': 'latitude_seconds',
    'Latitude Minutes': 'latitude_minutes',
    'Latitude Degrees': 'latitude_degrees',
    'Longitude Seconds': 'longitude_seconds',
    'Longitude Minutes': 'longitude_minutes',
    'Longitude Degrees': 'longitude_degrees',
    'Road Character': 'road_character',
    'Distance from Intersection': 'distance_from_intersection',
    'Total Un-Injured Persons': 'total_uninjured_persons_count',
    'Total Count of Persons Involved': 'total_person_involved_count',
    'Total Non-Fatal Injury Count': 'total_non_fatal_injury_count',
    'Total Fatality Count': 'total_fatality_count',
    'Total Pedestrian Count': 'total_pedestrian_count',
    'Total Pedalcyclist Count': 'total_pedalcyclist_count',
    'Total Unknown Non-Motorist Count': 'total_unknown_non_motorist_count',
    'Total Vehicle Occupant Count': 'total_vehicle_occupant_count'
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

def is_all_crash_id_valid(df):
    return (df.crash_id.isnull()).sum() == 0

def is_crash_month_limit_valid(df):
    return df.crash_month.dropna().between(JAN,DEC).all()

def is_lat_degree_valid(df):
    return df.latitude_degrees.dropna().between(41,47).all()

def is_week_day_code_limit_valid(df):
    return df.week_day_code.dropna().between(SUNDAY,SATURDAY).all()

def is_all_participant_id_unique(df):
    return df.participant_id.dropna().is_unique

def is_lat_degree_minute_seconds_valid(df):
    latitude_degrees = df.latitude_degrees
    latitude_minutes = df.latitude_minutes
    latitude_seconds = df.latitude_seconds
    all_not_null = latitude_degrees.notna() & latitude_minutes.notna() & latitude_seconds.notna() 
    all_null = latitude_degrees.isnull() & latitude_minutes.isnull() & latitude_seconds.isnull() 
    return (all_not_null | all_null).all()

def is_distance_from_intersection_valid(df):
    road_character = df.road_character.fillna(0)
    distance_from_intersection = df.distance_from_intersection.astype('float64').fillna(0.0)
    is_dist_right_for_road_char_0 = (road_character == 0) & (distance_from_intersection > 0.0)
    is_dist_right_for_road_char_1 = (road_character > 0) & (distance_from_intersection == 0.0)
    return (is_dist_right_for_road_char_0 | is_dist_right_for_road_char_1).all()

def is_all_serial_county_year_combination_unique(df):
    # set up crash_data frame
    crash_df=df[df['record_type'] == 1] 
    serial_no=crash_df['serial_no'].astype(str)
    county_code=crash_df['county_code'].astype(str)
    crash_year=crash_df['crash_year'].astype(str)
    return (serial_no + county_code + crash_year).is_unique

def is_all_crash_has_known_lat_long(df):
    # set up crash_data frame
    crash_df=df[df['record_type'] == 1] 
    has_lat = crash_df.latitude_degrees.notna() & crash_df.latitude_minutes.notna() & crash_df.latitude_seconds.notna() 
    has_long = crash_df.longitude_degrees.notna() & crash_df.longitude_minutes.notna() & crash_df.longitude_seconds.notna() 
    return (has_lat & has_long).all() 

def is_all_participant_id_has_crash_id(id):
    comparable_columns = ['crash_id','participant_id']
    # set up crash_participant_data frame
    crash_participant_df = df[comparable_columns]
    # remove rows with almost all missing data
    crash_participant_df = crash_participant_df.dropna(axis = 1, how ='all', thresh=2)
    # check if there is any null in crash id
    return crash_participant_df.crash_id.isnull().sum() == 0

def is_total_uninjured_count_valid(df):
    total_uninjured_persons_count=df['total_uninjured_persons_count'].fillna(0)
    total_person_involved_count=df['total_person_involved_count'].fillna(0)
    total_non_fatal_injury_count=df['total_non_fatal_injury_count'].fillna(0)
    total_fatality_count=df['total_fatality_count'].fillna(0)
    return (total_uninjured_persons_count == total_person_involved_count - (total_non_fatal_injury_count + total_fatality_count)).all()

def is_total_person_involved_count_valid(df):
    total_person_involved_count=df['total_person_involved_count'].fillna(0)
    total_pedestrian_count=df['total_pedestrian_count'].fillna(0)
    total_pedalcyclist_count=df['total_pedalcyclist_count'].fillna(0)
    total_unknown_non_motorist_count=df['total_unknown_non_motorist_count'].fillna(0)
    total_vehicle_occupant_count=df['total_vehicle_occupant_count'].fillna(0)
    return (total_person_involved_count == total_pedestrian_count + total_pedalcyclist_count + total_unknown_non_motorist_count + total_vehicle_occupant_count).all()

def is_crash_count_per_month_consistant(df):
    # group crashes by crash month and count the crash ids in each group
    crash_count_per_month_df = df.groupby(['crash_month'])['crash_id'].agg(['count'])
    crash_count_per_month = crash_count_per_month_df['count']
    percentile_10 = crash_count_per_month.quantile(0.1)
    percentile_90 = crash_count_per_month.quantile(0.9)
    mean = crash_count_per_month.mean()
    # check variation for more than 50%
    return (percentile_10 > (mean / 2)) & (mean > (percentile_90 / 2))

def is_crash_month_normally_distributed(id):
    # skewness of normal distribution should be 0. I am giving a tolerance range of .25
    return df.crash_month.skew() < 0.25

def is_crash_hour_normally_distributed(id):
    # Provide default hour of time for missing values
    crash_hour = df.crash_hour.fillna(0)
    # Replace wrong values as 0
    crash_hour = crash_hour.mask(crash_hour > 24, 0)
    # skewness of normal distribution should be 0. I am giving a tolerance range of .25
    return crash_hour.skew() < 0.25

def validateData():
    # Assertion 1: Existence Assertion
    # Assertion 1.a: All Records must have a record_type and the record_type should be either 1, 2 or 3
    if not is_all_record_types_valid(df):
        print("Existance Assertion Failed for record_type")

    # Assertion 1.b: All record must have a crash_id
    if not is_all_crash_id_valid(df):
        print("Existance Assertion Failed for crash_id")

    # Assertion 2: Limit Assertion
    # Assertion 2.a: Data in Crash month field should fall with in range 1 t0 12.
    if not (is_crash_month_limit_valid(df)):
        print("Limit Assertion Failed for crash_month")

    # Assertion 2.b: Data in Week Day Code field should fall with in range 1 t0 7.
    if not (is_week_day_code_limit_valid(df)):
        print("Limit Assertion Failed for week_day_code")

    # Assertion 2.c: When entered, Latitude Degrees must be a whole number between 41 and 47, inclusive
    if not (is_lat_degree_valid(df)):
        print("Limit Assertion Failed for latitude degree")

    # Assertion 3: Intra Record Check Assertion
    # Assertion 3a: Total Count of Persons Involved = Total Pedestrian Count + Total Pedalcyclist Count + Total Unknown Count + Total Occupant Count.
    if not is_total_person_involved_count_valid(df):
        print("Intra Record Assertion failed for Total Persons Count")

    # Assertion 3b: Total Un-Injured Persons Count = total number of persons involved - the number of persons injured - the number of persons killed
    if not is_total_uninjured_count_valid(df):
        print("Intra Record Assertion failed for Total Un-Injured Persons Count")
    
    # Assertion 4: Inter Record Check Assertion
    # Assertion 4a: Total crash should not vary more than 50% month on month
    if not is_crash_count_per_month_consistant(df):
        print("Inter Record Assertion failed for total crash")

    # Assertion 4b: Latitude Minutes must be null when Latitude Degrees is null
    # And Latitude Seconds must be null when Latitude Degrees is null
    if not is_lat_degree_minute_seconds_valid(df):
        print("Inter Record Assertion failed for latiude")
    
    # Assertion 4c: Distance from Intersection must = 0 when Road Character = 1
    # And Distance from Intersection must be > 0 when Road Character is not 1
    if not is_distance_from_intersection_valid(df):
        print("Inter Record Assertion failed for Distance from Intersection")
    
    # Assertion 5: Summary Assertion
    # Assertion 5a: Check if all participant has unique id
    if not (is_all_participant_id_unique(df)):
        print("Summary Assertion Failed for unique participant id")

    # Assertion 5b: Combination of Serial number + County + Year is unique
    if not (is_all_serial_county_year_combination_unique(df)):
        print("Summary Assertion Failed for unique Serial number + County + Year combination")

    # Assertion 6: Referential Integrity Assertion
    # Assertion 6a: Each participant id has a crash id
    if not is_all_participant_id_has_crash_id(df):
        print("Referential integrity Assertion Failed for participant_id:crash_id")

    # Assertion 6b: Every crash has a known lat long location
    if not is_all_crash_has_known_lat_long(df):
        print("Referential integrity Assertion Failed for crash_id:latitude:longitude")

    # Assertion 7: Statistical Distribution Assertion
    # Assertion 7a: Crashes should be normally distributed across all months
    if not is_crash_month_normally_distributed(df):
        print("Statistical Distribution Assertion Failed for crash month")

    # Assertion 7b: Crashes should be normally distributed throughout the day
    if not is_crash_hour_normally_distributed(df):
        print("Statistical Distribution Assertion Failed for crash hour")

    print("All validations passed successfully")

validateData()