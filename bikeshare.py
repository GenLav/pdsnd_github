import time
#from datetime import datetime
import pandas as pd
import numpy as np
import calendar

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
    month2 = ''
    day2 =''
    while True:
        cities = ['chicago', 'new york', 'washington']
        city = input('\nWould you like to see the data for Chicago, New York, Washington? \n').lower()
        if city not in cities:
            print('You may have mistyped that. Please try again ')
        else:
            print('\n{} it is!\n'.format(city.title()))
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june','all']
        month = input('Now type a month: January, February, March, April, May, June, or All \n').lower()
        if month not in months:
            print('Hmmm, thats odd. Please try again.')
        else:
            print('\n{}. Got it.\n'.format(month.title()))
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','all']
        day = input('Which day would you like to see? Sunday, Monday, etc..or type All \n').lower()
        if day in days:
            print('{} then. Lets get the data for you...'.format(day.title()))
            break
        else:
            print('Hmmm, thats odd. Please try again.')

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

def raw_data(df):
    """
    Displays first 5 lines of raw data upon user request
    """
    # user input to see if they want to see 5 lines of raw data
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    start_loc = 0

    while view_data == 'yes':
        print(df.iloc[0:5])

        start_loc += 5
        view_more_data = input("\nWould you like to view five more rows? Enter 'yes' or 'no'.\n").lower()

        if view_more_data == 'no':
            break
        else:
            if view_data not in ('yes', 'no'):
                print("\nThat's not quite right. Please type 'yes' or 'no'.\n")

print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    setmnth = set(df['month'])
    cnt = len(setmnth)
    if cnt >1:
        Common_mnth = df['month'].mode()[0]
        Common_mnth_display = calendar.month_name[Common_mnth]
        print('Most common month to ride is', Common_mnth_display)
    else:
        print('The most commom month stat can only be calculated for all months')

    # TO DO: display the most common day of week
    setday = set(df['day_of_week'])
    cnt2 = len(setday)
    if cnt2 >1:
        Common_day = df['day_of_week'].mode()[0]
        print('Most common day to ride is', Common_day)
    else:
        print('The most commom day stat can only be calculated for all days')

    # TO DO: display the most common start hour
    df['hr'] = df['Start Time'].dt.hour
    common_hr = df['hr'].mode()[0]
    if common_hr >=13:
        common_hr = common_hr-12
        print('Most common hour to ride is', common_hr,'PM')
    elif common_hr == 12:
        print('Most common hour to ride is', common_hr,'PM')
    else:
        print('Most common hour to ride is', common_hr,'AM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common starting station is ',common_start)
    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common ending station is ',common_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + ' - '+ df['End Station']
    common_startend = df['start_end'].mode()[0]
    print('Most common places to start and end is,',common_startend)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time sec_value = sec % (24 * 3600)
    seconds = df['Trip Duration'].sum() % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    duration =  "%d:%02d:%02d" % (hour, minutes, seconds)

    print('The total travel time is ', duration, 'Wow!')
    # TO DO: display mean travel time
    avg_seconds = df['Trip Duration'].mean() % (24 * 3600)
    avg_hour = avg_seconds // 3600
    avg_seconds %= 3600
    avg_minutes = avg_seconds // 60
    avg_seconds %= 60
    avg_duration =  "%d:%02d:%02d" % (avg_hour, avg_minutes, avg_seconds)
    print('The average travel time is ',avg_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #user_cnts = df.groupby(['User Type'])['User Type'].count()
    user_cnts = df['User Type'].value_counts()
    print('\nHere are the User counts. Note, it does not include null values\n', user_cnts)

    # TO DO: Display counts of gender
    #gender_cnts = df.groupby(['Gender'])['Gender'].count()
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nHere are the User counts by gender. Note, it does not include null values\n', gender_counts)
    except:
        print('Sorry, no gender data is available')

   
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min().astype(int)
        if earliest < 1900:
            print('\nThe earliest known Birth Year is', earliest,'But this may be a typing error...')
        else:
            print('\nThe earliest known Birth Year is', earliest)

        recent = df['Birth Year'].max().astype(int)
        print('\nThe most recent Birth Year is' , recent)

        common_bd = df['Birth Year'].mode()[0].astype(int)
        print('\nThe most common Birth Year is', common_bd)

    except:
        print('Sorry, no birth date data is available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
