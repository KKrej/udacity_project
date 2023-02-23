import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_check = {0: "all months",
                   1: "January",
                   2: "February",
                   3: "March",
                   4: "April",
                   5: "May",
                   6: "June",
                   7: "July",
                   8: "August",
                   9: "September",
                   10: "October",
                   11: "November",
                   12: "December"}

day_check = {0: "all days",
             1: "Monday",
             2: "Tuesday",
             3: "Wednesday",
             4: "Thursday",
             5: "Friday",
             6: "Saturday",
             7: "Sunday"}

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
    print("Please select one of the cities: chicago, new york city or washington?")
    city_check = ["chicago", "new york city", "washington"]

    while True:
        city = input("I choose: ").lower()
        if city in city_check:
            print("You selected: {}".format(city))
            break
        else:
            print("Please select one of the cities: chicago, new york city or washington?")
            continue


    # get user input for month (all, january, february, ... , june)
    print("Which month do you want to analise? Please type a number (all = 0).")


    while True:
        try:
            sel_month = int(input("I choose: "))
        except:
            print("This is not a number! Try again!")
            continue

        if sel_month in range(0,13):
            print("You selected: {}".format(month_check[sel_month]))
            break
        else:
            print("Please select a valid number.")
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("What day of week do you want to analise? Please type a number (all = 0).")


    while True:
        try:
            sel_day = int(input("I choose: "))
        except:
            print("This is not a number! Try again!")
            continue

        if sel_day in range(0, 8):
            print("You selected: {}".format(day_check[sel_day]))
            break

        else:
            print("Please select a valid number.")
            continue

    print('-'*40)

    month = month_check[sel_month]
    day = day_check[sel_day]
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
    df['Month'] = pd.to_datetime(df['Start Time']).dt.strftime("%B")
    df['Day of week'] = pd.to_datetime(df['Start Time']).dt.strftime("%A")

    if month == 'all months' and day == 'all days':
        df = pd.DataFrame(df)
    elif month == 'all months':
        df = pd.DataFrame(df[df['Day of week'] == day])
    elif day == 'all days':
        df = pd.DataFrame(df[df['Month'] == month])
    else:
        df = pd.DataFrame(df[(df['Day of week'] == day) & (df['Month'] == month)])

   # print("This is the data example we are looking into today for {}, {}, {}.".format(city, month, day))
    return df



def df_check(df):
    """ this function is checking if a data frame is not empty with users selections.
    If empty then exits the program entirely"""

    if df.empty:
        print("Sorry! Data not available")
        exit(1)
    else:
        answer = input('\nWould you like to see the top 5 rows of data? Type yes or no\n')
        if answer.lower() == 'yes':
            print(df.head())
            cnt = 5

        answer2 = 'yes'
        while answer2.lower() == 'yes':
            answer2 = input('\nShow next 5 raws of data? Type yes or no\n')
            print(df.iloc[cnt:cnt+5])
            cnt += 5



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month: %s' % df['Month'].mode()[0])

    # display the most common day of week
    print("The most common day of week: {}".format(df['Day of week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour: %s' % pd.to_datetime(df['Start Time']).dt.strftime("%H").mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station: %s' % df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station: %s' % df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df["Route"] = "from " + df['Start Station'] + " to " + df['End Station']
    print('The most commonly used route: %s' % df["Route"].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {} minutes, which is {} in hours or {} in days'
          .format(df['Trip Duration'].sum(), df['Trip Duration'].sum()/60, round((df['Trip Duration'].sum()/60)/24),2))

    # display mean travel time
    print('Mean travel time: %s minutes' % round(df['Trip Duration'].mean(), 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types')
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender
    print('\nCounts of gender')
    try:
        print(df['Gender'].value_counts().to_frame())
    except:
        print("This information is not available for this city!")

    # Display earliest, most recent, and most common year of birth
    print("\nYear of birth")
    try:
        print("The earliest: {}\nMost recent: {}\nMost common: {}"
              .format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))
    except:
        print("This information is not available for this city!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        df_check(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
