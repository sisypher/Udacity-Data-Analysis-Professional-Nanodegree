import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 
          'july', 'august', 'september', 'october', 'november', 'december']

days = { 'M' : 'Monday',
         'T' : 'Tuesday',
         'W' : 'Wednesday',
         'Th' : 'Thursday',
         'F' : 'Friday',
         'Sa' : 'Saturday',
         'Su' : 'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    city = input('Would you like to see data for Chicago, New York City, or Washington?\n').strip().lower()
    
    # in case the user inputs the string 'new york' and not 'new york city'
    if city == 'new york':
            city = 'new york city'
            
    while city not in CITY_DATA:
        city = input('\n\nYour input was invalid. Please Enter a city from the following: Chicago, New York City, or Washington\n').strip().lower()
        
    # default (no filters)
    day = 'all'
    month = 'all'
    
    time_filter = input('\n\nWould you like to filter the data by month, day, or not at all? Type \'none\' for no time filter\n').strip().lower()
    
    # get user input for month (all, january, february, ... , june)
    if time_filter == 'month':
        month = input('\n\nWhich month? January, February, March, April, May, or June? Please type out the full month name.\n').strip().lower()
        month = months.index(month) + 1
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif time_filter == 'day':
        day = input('\n\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su.\n').strip().title()
        if day not in days:
            print('\nYour Input was ivalid. Please enter a day from the following: M, Tu, W, Th, F, Sa, Su.')
        else:
            day = days[day]
    
    elif time_filter == 'none':
        # keep it as default
        day = 'all'
        month = 'all'
        
    print('Just one moment... loading the data for you')
    
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
    filename = CITY_DATA[city]
    
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['start hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month:', common_month)

    # display the most common day of week
    common_day = df['day'].mode()[0]
    print('\n\nThe most common day of week:', common_day)

    # display the most common start hour
    common_start_hour = df['start hour'].mode()[0]
    print('\n\nThe most common start hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('\nThe most frequent combination:\n', frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('User types counts:\n', user_types_counts)
        
    if 'Gender' in df.columns:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('\nGneder counts:\n', gender_counts)
        
    else:
        print('\nNo gender data to share.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year:', earliest_birth_year)

        earliest_birth_year = df['Birth Year'].max()
        print('\nMost recent birth year:', earliest_birth_year)

        common_birth_year = df['Birth Year'].mode()[0]
        print('\nMost common birth year:', common_birth_year)
    
    else:
        print('\nNo birth year data to share.')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    """Displays 5 rows of raw data."""
    
    display_status_list = ['yes', 'no']
    
    raw_data_display = ''
    
    counter = 0
    
    while raw_data_display not in display_status_list:
        raw_data_display = input('\nDo you want to see some raw data? yes or no?\n').strip().lower()
        if raw_data_display == 'yes':
                print(df.head())
                
        elif raw_data_display not in display_status_list:
            print('\nYour Input was Invalid. Please enter one one of the following: yes or no.\n')
    
    while raw_data_display == 'yes':
        raw_data_display = input('\nWould you like to see some more? yes or no.\n').strip().lower()
        
        if raw_data_display == 'yes':
            counter += 5
            print(df[counter:counter+5])
            
        elif raw_data_display == 'no':
            break

        elif raw_data_display not in display_status_list:
            raw_data_display = 'yes'
            print('\nYour Input was Invalid. Please enter one one of the following: yes or no.\n')
            
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()