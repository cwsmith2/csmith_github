import time
import pandas as pd
#changed 10/12/2024

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_valid_input(prompt, valid_inputs):
    """
    Repeatedly prompt the user until they provide valid input.

    Args:
        prompt (str): The message to display to the user.
        valid_inputs (dict): A dictionary of valid inputs and their corresponding values.

    Returns:
        str: The valid value selected by the user.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_inputs:
            return valid_inputs[user_input]
        print("Invalid input. Please try again.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city_shortcuts = {
        'ch': 'chicago',
        'ny': 'new york city',
        'wa': 'washington',
        'chicago': 'chicago',
        'new york city': 'new york city',
        'washington': 'washington'
    }

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_valid_input(
    "Please choose a city: Chicago (ch), New York City (ny), Washington (wa): ",
    city_shortcuts
)

    # Added all the months if other data is used.
    month_shortcuts = {
        'jan': 'january', '1': 'january', 'january': 'january',
        'feb': 'february', '2': 'february', 'february': 'february',
        'mar': 'march', '3': 'march', 'march': 'march',
        'apr': 'april', '4': 'april', 'april': 'april',
        'may': 'may', '5': 'may', 
        'jun': 'june', '6': 'june', 'june': 'june',
        'jul': 'july', '7': 'july', 'july': 'july',
        'aug': 'august', '8': 'august', 'august': 'august',
        'sep': 'september', '9': 'september', 'september': 'september',
        'oct': 'october', '10': 'october', 'october': 'october',
        'nov': 'november', '11': 'november', 'november': 'november',
        'dec': 'december', '12': 'december', 'december': 'december',
        '*': 'all', 'all':'all'
    }



    # get user input for month (all, january, february, ... , june)
    month = get_valid_input(
    "Choose a month to filter by: Jan, 1, February, ..., Dec, 12, or '*' for All: ",
    month_shortcuts
    )

    day_shortcuts = {
        'mon': 'monday', '1': 'monday', 'monday': 'monday',
        'tue': 'tuesday', '2': 'tuesday', 'tuesday': 'tuesday',
        'wed': 'wednesday', '3': 'wednesday', 'wednesday': 'wednesday',
        'thu': 'thursday', '4': 'thursday', 'thursday': 'thursday',
        'fri': 'friday', '5': 'friday', 'friday': 'friday',
        'sat': 'saturday', '6': 'saturday', 'saturday': 'saturday',
        'sun': 'sunday', '7': 'sunday', 'sunday': 'sunday',
        '*': 'all'
    }

    # Get user input for day of the week
    day = get_valid_input(
    "Choose a day to filter by: Mon, 1, Tuesday, ..., Sun, 7, or '*': ",
    day_shortcuts
    )


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    city_files
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data into DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Apply month filter
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december'].index(month) + 1
        df = df[df['month'] == month_index]

    # Apply day filter
    if day != 'all':
        df = df[df['day_of_week'] == day]   

    # Check if the filtered data is empty
    if df.empty:
        print("\nNo data found for the selected filters. Resetting filters...")
        return None

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most common month: {common_month}")

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most common day: {common_day}")

    # display the most common time for start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most common time for start hour: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(5) #pause for 5 seconds


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {common_start}")

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {common_end}")

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + " to " + df['End Station']
    common_route = df['route'].mode()[0]
    print(f"Most frequent trip: {common_route}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(5) #pause for 5 seconds


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_seconds = int(df['Trip Duration'].sum())
    hours, remainder = divmod(total_seconds, 3600)  # Get hours and remaining seconds
    minutes, seconds = divmod(remainder, 60)  # Get minutes and remaining seconds
    print(f"Total travel time: {hours} hours, {minutes} minutes, and {seconds} seconds")

    # display mean travel time
    mean_seconds = int(df['Trip Duration'].mean())
    avg_minutes, avg_seconds = divmod(mean_seconds, 60)  # Get minutes and remaining seconds
    print(f"Average travel time: {avg_minutes} minutes and {avg_seconds} seconds")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(5) #pause for 5 seconds


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Amount of User Types:")
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nTotal Gender entries:")
        print(df['Gender'].value_counts().to_string())
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Year of Birth: {earliest_year}")
        print(f"Most Recent Year of Birth: {recent_year}")
        print(f"Most Common Year of Birth: {common_year}")
    else:
        print("\nBirth Year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(5) #pause for 5 seconds

def display_raw_data(df):
    show_data = input("Would you like to see 5 lines of raw data? Enter yes or no.\n").strip().lower()
    start_loc = 0
    while show_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        show_data = input("Do you want to see 5 more lines of raw data? Enter yes or no.\n").strip().lower()


def main():
    while True:
        city, month, day = get_filters()

        # Loop until data is available for the selected filters
        while True:
            df = load_data(city, month, day)
            if df is not None:  # Data is found
                break
            # If no data, prompt user to reset filters
            city, month, day = get_filters()

        # Display the selected filters
        while True:
            print("\nYou selected the following filters:")
            print(f"City: {city.capitalize()}")
            print(f"Month: {month.capitalize() if month != 'all' else '* (All)'}")
            print(f"Day: {day.capitalize() if day != 'all' else '* (All)'}")
            print('-' * 40)

            reset = input("Do you want to proceed with these filters? Enter yes to proceed or no to reset.\n").strip().lower()
            if reset == 'yes':
                break
            elif reset == 'no':
                print("\nResetting filters...\n")
                city, month, day = get_filters()
            else:
                print("Invalid input. Please enter 'yes' to proceed or 'no' to reset.")
        # Load the filtered data
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
           print("\nThank you for using the program.\nHope to see you soon.")
           break


if __name__ == "__main__":
	main()
