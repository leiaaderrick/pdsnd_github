import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities=['chicago', 'new york', 'washington']
    while True :
        city=input('Would you like to view data from Chicago, New York or Washington?').strip().lower()
        print(city)
        if city in valid_cities:
            break 
        print("Invalid city, please choose from either New York, Washington or Chicago.")

    while True:
        time_period=input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.').strip().lower()
        if time_period in ['month','day','both','none']:
            break
        print('Invalid choice, please enter either day, month, both or none.')

    month= 'all'
    day= 'all'

    # TO DO: get user input for month (all, january, february, ... , june)
    if time_period in ['month', 'both']:
        months=['january', 'february', 'march','april','may','june']
        while True:
            month=input("enter the month:").strip().lower()
            if month in months:
                break
            print("Invalid month, please try again.")
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if time_period in ['day','both']:
        days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        while True:
            day= input("Enter day of the week:").strip().lower()
            if day in days:
                break
            print('Invalid day, please try again')

    if time_period == 'none':
        print('you\'ve entered none')
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']= pd.to_datetime(df['Start Time'])
    
    df['month']=df['Start Time'].dt.month_name().str.lower()
    df['day']=df['Start Time'].dt.day_name().str.lower()
    df['hour']=df['Start Time'].dt.hour
    if month !='all':
        df=df[df['month'] ==month]
        
    if day !='all':
        df=df[df['day'] ==day]
    
    return df
    

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    if month == 'all':
        mode_month= df['month'].mode()[0]
        print(f'The most popular month is {mode_month}') 
  

    # TO DO: display the most common day of week
    if day == 'all':
        mode_day=df['day'].mode()[0]
        print(f'The most popular day is {mode_day}')
    
    # TO DO: display the most common start hour
    mode_hour=df['hour'].mode()[0]
    print(f'The most popular hour is {mode_hour}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mode_st_station= df['Start Station'].mode()[0]
    print(f'The most commonly used starting point is {mode_st_station}.')

    # TO DO: display most commonly used end station
    mode_end_station= df['End Station'].mode()[0]
    print(f'The most commonly used end station is {mode_end_station}.')

    # TO DO: display most frequent combination of start station and end station trip
    common_trip= df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'The most frequent trip starts at {common_trip[0]} and ends at {common_trip[1]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Duration (min)']= df['Trip Duration'] / 60
    
    # TO DO: display total travel time
    total_travel_time = df['Duration (min)'].sum()
    hours = int(total_travel_time // 60)
    minutes = int(total_travel_time % 60)
    print(f'The total time spent travelling is {hours} hours and {minutes} minutes.')

    # TO DO: display mean travel time
    mean_travel_time = df['Duration (min)'].mean()
    print(f'The average trip duration is {mean_travel_time} minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types= df['User Type'].value_counts()
    print('User Type Count:\n', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts)
    else:
        print('There is no data available for gender.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_BY = int(df['Birth Year'].min())
        most_recent_BY = int(df['Birth Year'].max())
        most_common_BY = int(df['Birth Year'].mode()[0])
        
        print(f'The earliest birth year is {earliest_BY}.')
        print(f'The most recent birth year is {most_recent_BY}.')
        print(f'The most common birth year is {most_common_BY}.')
    else:
        print('There is no data available regarding birth year.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    start_loc = 0
    while True:
        see_data = input("\nWould you like to see the raw data? Enter 'Yes' or 'No': ").strip().lower()
        if see_data != 'yes':
            break
        print(df.iloc[start_loc: start_loc +5])
        start_loc +=5
        
        if start_loc > len(df):
            print('You have reached the end of the data')
            break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
       

if __name__ == "__main__":
	main()
