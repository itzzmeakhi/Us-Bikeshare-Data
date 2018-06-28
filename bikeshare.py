import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago':'chicago.csv',
             'washington':'washington.csv',
             'new_york':'new_york_city.csv'}
""" Defining dictionary key as city names and values as respective csv file's to
access them according to the user input """

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello..!! Let's explore some US bikeshare data ")
    print("Which city you want to see data for Chicago, Washington and New York")

    city = input()
    """ To get user input for the city """
    city_name = city.lower().replace(' ','_')
    """ To convert city name into lower and replace spaces with underscore """
    while city_name not in CITY_DATA:
        """ To handle invalid input entered by the user """
        print("Your entered city %s is invalid " % (city_name))
    print("Selected City is %s " % (city_name))

    print("Would you like to filter data by month, day, both, or not at all? Type 'none' for no")
    choice_data = ['month','day','both','none']
    data_choice = input()
    """ To get user input for the choice """
    choice = data_choice.lower()
    """ To convert the choice into lower case """
    while choice not in choice_data:
        """ To handle invalid input entered by the user """
        print("Your entered choice %s is invalid " % (choice))

    if choice == 'month':
        """ If Selected Choice is month """
        print("Which month? January, February, March, April, May, June")
        month = input()
        month = month.lower()
        day_of_week = 'all'
    elif choice == 'day':
        """ If Selected Choice is day """
        print("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday ")
        day_of_week = input()
        month = 'all'
    elif choice == 'both':
        """ If the Selected Choice is both """
        print("Which month? January, February, March, April, May, June")
        month = input()
        month = month.lower()
        print("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday ")
        day_of_week = input()
    else:
        """ If Selected Choice is none """
        month = 'all'
        day_of_week = 'all'

    print('-'*100)
    """ To print a straight line """
    return city_name,month,day_of_week

def load_data(city,month,day):
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
    """ To load the selected city csv file """

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    """ To convert start time into standard time """
    df['month'] = df['Start Time'].dt.month
    """ To get the month value from start time """
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    """ To get the day_of_week value from start time """

    if month != 'all':
        """ If selected month is not none in choice then this function will triggers """
        months = ['january','february','march','april','may','june']
        """ List of months """
        month = months.index(month)+1
        """ Find the index of selected month from the list """
        df = df[df['month'] == month]
        """ New DataFrame that contains the old data frame month equals to selected month """

    if day != 'all':
        """ If selected day is not none in choice then this function will triggers """
        df = df[df['day_of_week'] == day.title()]
        """ New DataFrame that contains the old data frame day equals to selected day """

    print('-'*100)
    """ To print a straight line """
    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""
    print("Calculating the Most Frequent Time's of travel")
    start_time = time.time()
    """ Time while triggering the function """

    frequent_month = df['Start Time'].dt.month.mode()[0]
    """ Frequent month from the data set """

    frequent_day = df['Start Time'].dt.weekday_name.mode()[0]
    """ Frequent day from the data set """

    frequent_hour = df['Start Time'].dt.hour.mode()[0]
    """ Frequent hour from the data set """

    print("The Most Frequent Month is %s " % (frequent_month))
    print("The Most Frequent Day is %s " % (frequent_day))
    print("Most Frequent Hour is %s " % (frequent_hour))

    print("This took %s seconds" % (time.time() - start_time))
    """ To calculate the total time took for processing above results """
    print('-'*100)
    """ To print a straight line """

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""
    print("Calculating the Most Frequent Station's of travel")
    start_time = time.time()
    """ Time while triggering the function """

    frequent_start_station = df['Start Station'].mode()[0]
    """ Frequent start station from the data set """

    frequent_end_station = df['End Station'].mode()[0]
    """ Frequent end station from the data set """

    trip_with_counts = df.groupby(['Start Station','End Station']).size().reset_index(name = 'trips')

    sort_trips = trip_with_counts.sort_values('trips', ascending = False)

    start_trip = sort_trips['Start Station'].iloc[0]

    end_trip = sort_trips['End Station'].iloc[0]
    """ Frequent Trip Route from the data set """

    print("Most Frequent Start Station is %s " % (frequent_start_station))
    print("Most Frequent End Station is %s " % (frequent_end_station))
    print("Most popular trip is from %s to %s " % (start_trip,end_trip))

    print("This took %s seconds" % (time.time() - start_time))
    """ To calculate the total time took for processing above results """
    print('-'*100)
    """ To print a straight line """

def trip_duration_stats(df):

    """Displays statistics on the total and average trip duration."""
    print("Calculating Trip Duration...!")
    start_time = time.time()
    """ Time while triggering the function """

    total_trip_time = df['Trip Duration'].sum()
    """ Total trip time """

    mean_trip_time = df['Trip Duration'].mean()
    """ Mean trip time """

    print("Total Travel Time is %s in seconds " % (total_trip_time))
    print("Mean Travel Time is %s in seconds " % (mean_trip_time))

    print("This took %s seconds" % (time.time() - start_time))
    """ To calculate the total time took for processing above results """
    print('-'*100)
    """ To print a straight line """

def user_stats(df,city):

    """Displays statistics on bikeshare users."""
    print("Calculating User stats..!")
    start_time = time.time()
    """ Time while triggering the function """

    print("Count's of User Type's ")

    if 'User Type' in df.columns:
        """ To handle exception if User Type data is unavailable in the dataset """
        print(df['User Type'].value_counts())
    else:
        print("Oops..! for %s User Type data is not available " % (city))


    print("Count's of Gender ")

    if 'Gender' in df.columns:
        """ To handle exception if Gender data is unavailable in the dataset """
        print(df['Gender'].value_counts())
    else:
        print("Oops..! for %s Gender data is not available " % (city))

    print(" Stats regarding Birth Year data ")
    
    if 'Birth Year' in df.columns:
        """ To handle exception if Birth Year data is unavailable in the dataset """
        max_birth_year = df['Birth Year'].max()

        print("Most Recent Birth Year is %s " % (max_birth_year))

        min_birth_year = df['Birth Year'].min()

        print("Most Earliest Birth Year is %s " % (min_birth_year))

        frequent_birth_year = df['Birth Year'].mode()[0]

        print("Most Frequent Birth Year is %s " % (frequent_birth_year))
    else:
        print("Oops..! for %s Birth Year data is not available " % (city))
    print('-'*100)
    """ To print a straight line """

def main():
    while True:
        city,month,day = get_filters()
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        print("Would you like see five rows of data ?? Enter yes or no ")
        display_data = input()
        display_data = display_data.lower()

        i = 5
        while display_data == 'yes':
            """ To display few rows of data for user view """
            print(df[:i])
            print("Would you like to see five more rows of data ?? Enter yes or no ")
            i *= 2
            display_data = input()
            display_data = display_data.lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
