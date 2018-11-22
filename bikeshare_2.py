import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    correct_city = False
    cities = ['chicago', 'new york city', 'washington']
    while(not correct_city):
        city = input("Enter the name of the city (chicago, new york city, washington): ").lower()
        if(city in cities):
                correct_city = True

    #get user input for month (all, january, february, ... , june)
    correct_month = False
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december']
    while(not correct_month):
        month = input("\nEnter the month (all, january, february, ... , june): ").lower()
        if(month in months):
                correct_month = True

    #get user input for day of week (all, monday, tuesday, ... sunday)
    correct_day = False
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while(not correct_day):
        day = input("\nEnter the day of week (all, monday, tuesday, ... sunday): ").lower()
        if(day in days):
                correct_day = True


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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print("Most common month: {}".format(common_month))

    #display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day = df['day_of_week'].mode()[0]
    print("Most common day of week: {}".format(common_day))

    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most common start hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    com_start_station = df['Start Station'].mode()[0]
    print("The most common Start Station is: {}".format(com_start_station))

    #display most commonly used end station
    com_end_station = df['End Station'].mode()[0]
    print("The most common End Station is: {}".format(com_end_station))

    # display most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station','End Station'])['Start Station'].agg(['count']).sort_values('count', ascending = False).head(1).reset_index()
    print("The most common trip is:\n\n {}".format(common_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: {}".format(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Check if column 'User Type' is in dataframe
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print(user_types)
    else:
        print("\nNo User Type information")
    #Check if column 'Gender' is in dataframe
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("\nNo Gender Information")
    #Check if column 'Birth Year' is in dataframe
    if 'Birth Year' in df.columns:
        earliest_month = df['Birth Year'].min()
        recent_month = df['Birth Year'].max()
        common_month = df['Birth Year'].mode()[0]
    else:
        print("No Birth Year information")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
