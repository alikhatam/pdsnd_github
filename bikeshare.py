import time
import calendar
import pprint
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
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Which city do you want to analyze its bikeshare data: Chicago, New York City, or Washington?\n")
        if city.lower() not in ["chicago", "new york city" ,"washington"]:
            print("You didn't select one of the three valid city names!")
        else:
            break

    # get user input for filter options
    while True:
        filter = input("Would you like to filter the data by month, day, both or not at all?\nType month, day, both, or no.: ")
        if filter.lower() == 'both':
            month = filter_month()
            day = filter_day()
            break
        elif filter.lower() == 'month':
            month = filter_month()
            day = 'all'
            break
        elif filter.lower() == 'day':
            month = 'all'
            day = filter_day()
            break
        elif filter.lower() == 'no':
            month = 'all'
            day = 'all'
            break
        else:
            print("You didn't select a valid option!")

    print('-'*40)
    return city, month, day

def filter_month():
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month do you want to filter by? Type \"all\" for no month filter.\n")
        month_list = ["january", "february", "march", "april", "may", "june"]
        if month.lower() not in month_list and month.lower()!="all":
            print("The month name is not recognized!")
        else:
            return month
            break

def filter_day():
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of week do you want to filter by? Type \"all\" for no day filter.\n")
        day_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        if day.lower() not in day_list and day.lower()!="all":
            print("The day name is not recognized!")
        else:
            return day
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month(s)
    if month == "all":
        common_month = df['month'].mode().tolist()
        common_month_name = [calendar.month_name[common_month[i]] for i in range(len(common_month))]
        common_month_count = df[df['month']==common_month[0]].count()[0]
        print("\nPopular month(s): {} ({} counts)".format(common_month_name, common_month_count))

    # display the most common day of week(s)
    if day == "all":
        common_dow = df['day_of_week'].mode().tolist()
        common_dow_count = df[df['day_of_week']==common_dow[0]].count()[0]
        print("\nPopular day(s) of week: {} ({} counts)".format(common_dow, common_dow_count))


    # display the most common start hour(s)
    common_hour = df['hour'].mode().tolist()
    common_hour_count = df[df['hour']==common_hour[0]].count()[0]
    print("\nPopular start hour(s): {} ({} counts)".format(common_hour, common_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station(s)
    common_startstation = df['Start Station'].mode().tolist()
    common_startstation_count = df[df['Start Station']==common_startstation[0]].count()[0]
    print("\nPopular start station(s): {} ({} counts)".format(common_startstation, common_startstation_count))


    # display most commonly used end station(s)
    common_endstation = df['End Station'].mode().tolist()
    common_endstation_count = df[df['End Station']==common_endstation[0]].count()[0]
    print("\nPopular end station(s): {} ({} counts)".format(common_endstation, common_endstation_count))


    # display most frequent combination(s) of start station and end station trip
    df['Station Comb'] = df['Start Station'] + ' --> ' + df['End Station']
    common_station_comb = df['Station Comb'].mode().tolist()
    common_station_comb_count = df[df['Station Comb']==common_station_comb[0]].count()[0]
    print("\nPopular trip(s): {} ({} counts)".format(common_station_comb, common_station_comb_count))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total travel time: {} ({} counts)'.format(df['Trip Duration'].sum(), df.count()[0] ))

    # display mean travel time
    print('\nThe mean travel time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nThe breakdown of users:\n' + df['User Type'].value_counts().to_string())

    # display gender and year of birth stats if city is not Washington
    if city.lower() != 'washington':
        # Display counts of gender
        print('\nThe breakdown of gender:\n' + df['Gender'].value_counts().to_string())

        # Display earliest, most recent, and most common year of birth
        print('\nThe earliest year of birth:', int(df['Birth Year'].min()))
        print('\nThe most recent year of birth:', int(df['Birth Year'].max()))
        common_year = df['Birth Year'].mode().tolist()
        print('\nThe most common year(s) of birth:', list(map(int, common_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def diplay_data(df):
    """prompt the user if they want to see 5 lines of raw data,
    display that data if the answer is 'yes',
    and continue these prompts and displays until the user says 'no'.
    """
    pp = pprint.PrettyPrinter(indent=1)
    i = 0
    while True:
        display = input("\nWould you like to view the data for the next five trips? Enter yes or no.\n")
        if display.lower() == "yes":
            dict_list = df[i:i+5].to_dict('records')
            pp.pprint(dict_list)
            i += 5
        else:
            print('='*40)
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        df = df.drop(['month', 'day_of_week', 'hour', 'Station Comb'], axis=1)
        diplay_data(df)

        restart = input('\n\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
