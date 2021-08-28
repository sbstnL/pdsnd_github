import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input(
            "\n Which city do you want to analyze? You can chose from Chicago, New York City or Washington \n").lower()
        if city in cities:
            break
        else:
            print("\n Please enter a valid city.")

        # get user input for month (all, january, february, ... , june)
    while True:
        months = ['all', 'january', 'february',
                  'march', 'april', 'may', 'june']
        month = input("For which month would you like to see the data? Use January, February, March, April, May or June. You can type 'all' if you do not want a month filter.\n").lower()
        if month in months:
            break
        else:
            print(
                "Please enter a valid month: January, February, March, April, May, June")

        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all', 'monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
        day = input("For which day of the week would you like to see the data? Use Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. If you do not want to select a day you can type all.\n").lower()
        if day in days:
            break
        else:
            print("Please enter a valid day.")

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

  # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = months[popular_month-1]
        print(popular_month, "is the most common month")

    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print(popular_day, "is the most common day of the week")

        # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    print("The popular Start Hour is at {}:00 hrs".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))


print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(popular_start_station, "is the most common start station")
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(popular_end_station, "is the most common end station")

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print(popular_combination,
          "is the most common combination of start and end station")

    print("\nThis took %s seconds." % (time.time() - start_time))


print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum())
    #Finds out the duration in minutes and seconds format
    minute, second = divmod(total_travel_time, 60)
    #Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"{hour}:{minute}:{second} (hours : minutes : seconds) is the total travel time")
    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    #Finds out the duration in minutes and seconds format
    mins, secs = divmod(mean_travel_time, 60)
    #This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"{hrs}:{mins} (hours : minutes) is the mean travel time")
    else:
        print(f"{mins}:{secs} (minutes : seconds) is the mean travel time")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print("These are the user types: \n", user_types)
    # Display counts of gender if city has gender information
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("These are the genders: \n", gender)
    else:
        print("Gender: There is no gender information in this city")

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df:
        earliest_birth = int(df['Birth Year'].min())
        latest_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print(
            f"The oldest user was born in {earliest_birth}, the youngest user in {latest_birth}, and the most common birth year is {most_common_birth}")
    else:
        print("Birth year: This city does not have any data about the birth year of their users")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Asks user if they want to see raw data"""
    i = 0
    user_question = input(
        'Would you like to see the raw data?\n type yes or no').lower()

    while user_question in ['yes', 'y', 'yep', 'yea'] and i+5 < df.shape[0]:
        print(df.iloc()[i:i+5])
        i += 5
        user_question = input(
                'Would you like to see more data? Please enter yes or no:').lower()
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
