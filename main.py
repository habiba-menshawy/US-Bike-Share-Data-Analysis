import time
import pandas as pd
import numpy as np
import statistics

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

def validate_data(prompt,valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted
    Returns:
        (str) user_input - the user's valid input
    """
    user_input = prompt.lower()
    while user_input not in valid_entries :
            user_input = input("Please enter a valid choice from "+str(valid_entries)+" : ").lower()
    return user_input



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
    city = input("Please enter a name of a city from [Chicago, New York, Washington]: ")
    city = city.lower()
    city=validate_data(city,CITY_DATA.keys())
    # Asking the user for the filters to apply
    filter = input("would you like to filter data by month, day, both or none? ")
    filter = filter.lower()

    # list of available filters
    filters = ['both', 'none', 'day', 'month']
    filter=validate_data(filter , filters)
    # TO DO: get user input for month (all, january, february, ... , june)
    month = "All"
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    # Assigning the month filter
    if (filter == 'both' or filter == 'month'):
        month = (input('Please enter the name of the month to filter by: '))
        month = month.lower()
        # handling wrong input
        month = validate_data(month, months)
    month = month.capitalize()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = "All"

    week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # Assigning the day filter
    if (filter == 'both' or filter == 'day'):
        day = input('Please enter a name of the day of week to filter by: ')
        day = day.lower()
        # handling wrong input
        day= validate_data(day, week)

    day = day.capitalize()
    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    # Changing the 'Start Time' to date format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Applying the month filter
    if (month != 'All'):
        df = df[df['Start Time'].dt.month_name() == month]

    # Applying the day filter
    if (day != 'All'):
        df = df[df['Start Time'].dt.day_name() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month: " + str(df['Start Time'].dt.month_name().mode()[0]))

    # TO DO: display the most common day of week
    print("Most common day of week: " + str(df['Start Time'].dt.day_name().mode()[0]))

    # TO DO: display the most common start hour
    print("Most common start hour: " + str(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most commonly used start station: " + str(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most commonly used end station: " + str(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip: "
          + str(("\n Start Station: " + df['Start Station'] + "\n End Station: " + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time: " + str(df["Trip Duration"].sum()))

    # TO DO: display mean travel time
    print("The average travel time: " + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User Types value counts:")
    print(df["User Type"].value_counts().to_string(), "\n")

    # TO DO: Display counts of gender
    print("Gender value counts:")

    if 'Gender' not in df.columns:
        print("No gender data available \n")
    else:
        print(df['Gender'].value_counts().to_string())

    # TO DO: Display earliest, most recent, and most common year of birth
    print("Birth Year stats:")

    if "Birth Year" not in df.columns:
        print("No birth year data available \n")
    else:
        print("Earliest year of birth: " + str(int(df["Birth Year"].min())))
        print("The most recent year of birth: " + str(int(df["Birth Year"].max())))
        print("The most common year of birth: " + str(int(df["Birth Year"].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """
        Ask the user whether he wants to see 5 rows of data continuously
        Args:
            (df) the data frame to be shown
        prints:
            5 rows of data continuously as much as the user would like
        """
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    view_data.lower()
    ans = ["yes", "no"]
    view_data = validate_data(view_data, ans)
    start_loc = 75826
    while (view_data == "yes"):
        # printing 5 rows of the data as long as there are 5 rows to be shown
        if (start_loc+5 <= df.shape[0]):
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to show 5 more rows?: ").lower()
            view_data = validate_data(view_data, ans)
        # In case that the user reached the end of the data and wants to start over
        elif(start_loc >= df.shape[0]):
            view_data = input("The data is finished would you like to start over?\n").lower()
            view_data = validate_data(view_data, ans)
            if(view_data=="yes"):
              start_loc = 0
        # printing the rest of the rows of the data in case there are less than 5 rows of data
        # and asking if the user wants to start over
        elif(start_loc < df.shape[0]):
            print(df.iloc[start_loc:])
            view_data = input("The data is finished would you like to start over?\n").lower()
            view_data = validate_data(view_data, ans)
            if (view_data == "yes"):
                start_loc = 0


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
