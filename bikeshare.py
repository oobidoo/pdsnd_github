#import necessary packages
import time
import numpy as np
import pandas as pd
from calendar import month_name
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    global city

    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Please type the city you would like to get more insights on:\n''\nChicago, New York City or Washington, in full: ')
    while True:
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input().lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            print('You chose {}.'.format(city))
            break
        else:
            print('Please type in Chicago, New York City or Washington.')
    
    return city

def get_month():
    global month
    while True:
        month = input('Do you want to filter by a specific month between January and June, or by all: ')
        month = month.lower()
        if month not in ('january','february','march','april','may','june','all'): # 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may'or month == 'june' or month == 'all':
            #print('Selection noted as: {}.'.format(month))
            print('Do you want to filter by a specific month between January and June, or by all:')
        else:
            print('Month selection noted as: {}.'.format(month))
            break
    return month

def get_day():
    global day
    while True:
        day = input('Do you want to filter by a specific day between Monday and Sunday, or by all: ').lower()
        day = day.lower()
        if day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all':
            print('Day selection noted as: {}.'.format(day))
            break
        else:
            print('Do you want to filter by a specific day between Monday and Sunday, or by all: ')
    return day

def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def popular_times(df):
    print('----Displaying popular time statistics----')
    start_time = time.process_time()
    
    # popular month
    #Reference : https://stackoverflow.com/questions/36010999/convert-pandas-datetime-month-to-string-representation
    df['month']= df['Start Time'].dt.strftime('%b')
    pop_month= df['month'].mode()[0]
    #https://stackoverflow.com/questions/15138973/how-to-get-the-number-of-the-most-frequent-value-in-a-column/30063996
    pop_month_count =df['month'].value_counts().max()
    str_pop_month_count=str(pop_month_count)
    print('The most popular month is: '+ pop_month+ ' occurring '+str_pop_month_count+' times.')	
   
    # popular day of week  
    df['day_of_week']= df['Start Time'].dt.weekday_name
    pop_day= df['day_of_week'].mode()[0]
    pop_day_count =df['day_of_week'].value_counts().max()
    str_pop_day_count=str(pop_day_count )
    print('The most popular day is: '+ pop_day+' occurring '+str_pop_day_count+' times.')
    
    # popular start hour
    #https://stackoverflow.com/questions/42977395/pandas-dt-hour-formatting
    df['hour']= df['Start Time'].dt.strftime('%H').add(':00:00')
    pop_hour = df['hour'].mode()[0]
    pop_hour_count =df['hour'].value_counts().max()
    str_pop_hour_count=str(pop_hour_count)
    print('The most popular start hour is: '+ pop_hour+' occurring '+str_pop_hour_count+' times.')
    process_time = str(time.process_time() - start_time)
    print('This took ' + process_time+' seconds')
    print('*_______________________________________*')
def popular_stations(df):
    print('----Displaying popular station statistics----')
    start_time = time.process_time()
    
    #popular start station
    pop_start_station=df['Start Station'].mode()[0]
    pop_start_station_count=df['Start Station'].value_counts().max()
    str_pop_start_station_count=str(pop_start_station_count)
    print('The most popular start station is: '+ pop_start_station+' occurring '+str_pop_start_station_count+' times.')
    
    #popular end station
    pop_end_station=df['End Station'].mode()[0]
    pop_end_station_count=df['End Station'].value_counts().max()
    str_pop_end_station_count=str(pop_end_station_count)
    print('The most popular end station is: '+ pop_end_station+' occurring '+str_pop_end_station_count+' times.')
    
    #popular trip 
    df ['Trip Name']= df['Start Station'] +' '+'to'+' '+df['End Station']
    pop_trip= df ['Trip Name'].mode()[0]
    pop_trip_count=df ['Trip Name'].value_counts().max()
    str_pop_trip_count=str(pop_trip_count)
    print('The most popular trip is: '+ pop_trip+' occurring '+str_pop_trip_count+' times.')
  
    process_time = str(time.process_time() - start_time)
    print('This took ' + process_time +' seconds')
    print('*_______________________________________*')

def trip_durations(df):
    print('----Displaying trip statistics----')
    start_time = time.process_time()
    
    #total trip duration
    raw_total_trip_duration=df['Trip Duration'].sum()
    #https://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days/38222840
    sec=timedelta(seconds=int(raw_total_trip_duration))
    str_sec=str(sec)
    print('The total trip duration for selected period is: '+str_sec +' (hrs:mins:secs)')

    #average trip duration
    avg_trip_duration=df['Trip Duration'].mean()
    avg_sec=timedelta(seconds=int(avg_trip_duration))
    str_avg_sec=str(avg_sec)
    print('The average trip duration for selected period is: '+str_avg_sec +' (hrs:mins:secs)')
    process_time = str(time.process_time() - start_time)
    print('This took ' + process_time+' seconds')
    print('*_______________________________________*')

def user_details(df):
    print('----Displaying user statistics----')
    start_time = time.process_time()

    #counts of user types
    count_user_types=df['User Type'].value_counts()
    str_count_user_types=str(count_user_types)
    print(str_count_user_types)

    if city == 'chicago' or city == 'new york city':
    #counts of each gender
        count_gender_types=df['Gender'].value_counts()
        str_count_gender_types=str(count_gender_types)
        print(str_count_gender_types)

    #earliest, most recent, most common year of birth 
        earliest_birth=df['Birth Year'].min()
        latest_birth=df['Birth Year'].max()
        common_birth=df['Birth Year'].mode()[0]
        #https://stackoverflow.com/questions/35614496/how-to-remove-the-0-in-a-integter-in-python
        print('The earlies, latest and most common birth years are: {}, {} and {} '.format(int(earliest_birth),int(latest_birth),int(common_birth)))
        
    process_time = str(time.process_time() - start_time)
    print('This took ' + process_time+' seconds')
    print('*_______________________________________*')

def display_code(df):
    five_lines=df
    row_index=0
    user_choice=input('Would you like to see 5 more rows of raw data (yes or no)?: '.lower())
    while True:
        if user_choice == 'no':
            return
        if user_choice=='yes':
            print(five_lines[row_index: row_index+5])
            row_index = row_index+5
        user_choice=input('Would you like to see 5 more rows of raw data (yes or no)?: ').lower()

def main():
    while True:
        city = get_city()
        month=get_month()
        day=get_day()
        df=load_data(city,month, day)
        popular_times(df)
        popular_stations(df)
        trip_durations(df)
        user_details(df)
        display_code(df)
        restart = input('Do you want to perform another analysis (yes or no)?')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()

