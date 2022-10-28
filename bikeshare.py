# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:00:57 2022

@author: Sven-Olof Andersson
"""

import pandas as pd
import math

def get_filters():
    """Get the filters used in the analysis (city, month, weekday)"""
    
    print("Welcome to the anlysis of some bikeshare data")
    print("You must select a city and you can also select a specific month and/or weekday")
    print()
    city_names = {"C": "Chicago", "N": "New York", "W": "Washington"}
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    
    
    #Get the city filter (mandatory)
    while True:
        select_city = input("Enter the first character to select a city, C - Chicago, N - New Yourk or W - Washington: ").upper()
        if len(select_city) != 1:
            print()
            print("You cannot enter ", select_city, "Please try again and enter one letter to select a city")
        elif select_city not in city_names:
            print()
            print("You must select C, N or W for Chicago, New York or Washington")
        else:
            city = city_names[select_city]
            break
            
    #Get the month filter (optional)
    while True:
        month = input("Please enter a month to use a month filter or press enter to not filter on month: ").title()
        if month in months or month == "":
            break
        else:
            print()
            print("Please enter a full month name or press Enter for all")
            
    #Get the weekday filter (optional)
    while True:
        print()
        weekday = input("Please enter a weekday to use a weekday filter or press enter to not filter on weekday: ").title()
        if weekday in weekdays or weekday == "":
            break
        else:
            print()
            print("Please enter a weekday name or press Enter for all")
            
    if month == "":
        month = "All"
        
    if weekday == "":
        weekday = "All"
        
    return city, month, weekday

        

def load_data (city, month, weekday):
    """ Read data for one city and add information about hour, month and weekday """
    
    cities = {"Chicago": "chicago.csv", "New York": "new_york_city.csv", "Washington":"washington.csv"}
    month_name = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
    day_name={0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    
    df = pd.read_csv(cities[city])
    
    # Convert Start Time to date-time format
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    
    # Add a column with hours
    df["Hour"] = df["Start Time"].dt.hour
    
    # Add a column with month number
    df["Month"] = df["Start Time"].dt.month.map(month_name)
    
    # Add a column with day of week
    df["Day of Week"] = df["Start Time"].dt.weekday.map(day_name)
    
    #Filter out month    
    if month != "All":
        df = df[df["Month"] == month]
        
    #Filter out weekday    
    if weekday != "All":
        df = df[df["Day of Week"] == weekday]
    
    return df

def time_stat(df):
    
    """ Find the most popular hors, day and month to rent a bike """
    
    # Find the most popular hour and the number of rentals for that our by sorting counting and taking the top result
    
    popular_hour = df["Hour"].value_counts().iloc[:1]
    hour = popular_hour.axes[0][0]
    hour_rentals = popular_hour.iloc[0]
    
    # Find the most popular day and the number of rentals for that our by sorting counting and taking the top result
    
    popular_day = df["Day of Week"].value_counts().iloc[:1]
    day = popular_day.axes[0][0]
    day_rentals = popular_day.iloc[0]
    
    # Find the most popular month and the number of rentals for that our by sorting counting and taking the top result
    
    popular_month = df["Month"].value_counts().iloc[:1]
    month = popular_month.axes[0][0]
    month_rentals = popular_month.iloc[0]
    
    return hour, hour_rentals, day, day_rentals, month, month_rentals

def station_stat(df):
    
    """ Find the most popular stations """
       
    # Find the most popular start station
    
    popular_start = df["Start Station"].value_counts().iloc[:1]
    start_station = popular_start.axes[0][0]
    start_rentals = popular_start.iloc[0]
    
    # Finde the most popular end station
    
    popular_end = df["End Station"].value_counts().iloc[:1]
    end_station = popular_end.axes[0][0]
    end_rentals = popular_end.iloc[0]
    
    # Create a new coulm with the combination of start and end station, then fins the most popular one
    
    df["Stations"]=df["Start Station"] + " to " + df["End Station"]
    popular_journey = df["Stations"].value_counts().iloc[:1]
    journey = popular_journey.axes[0][0]
    journey_rentals = popular_journey.iloc[0]
    
    return start_station, start_rentals, end_station, end_rentals, journey, journey_rentals

def trip_duration(df):
    
    """ Calculate the total travel time and the average traveltime """
    
    # Total travel time
    
    tot_time = df["Trip Duration"].sum()
    
    # Average (mean) trip time
    
    trip_mean = math.trunc(round(df["Trip Duration"].mean(), 0))
    
    return tot_time, trip_mean

def user_info(df, city):
    
    """ Information abouty the users of the bikes """
    
    # Count the number of users within each user type
    
    users = df["User Type"].value_counts()
    
    # Count the numbers within each gender, excpet for Washington where no such information is available
    # Get fata about the birth date, also not available for Washington
    
    if city == "Washington":
        gender = "No gender data available"
        oldest = 0
        youngest = 0
        common_bd = 0
        rentals_age = 0
    else:
        gender = df["Gender"].value_counts()
        oldest = df["Birth Year"].min()
        youngest = df["Birth Year"].max()
        common_bd = df["Birth Year"].value_counts().iloc[:1].axes[0][0]
        rentals_age = df["Birth Year"].value_counts().iloc[:1].iloc[0]
        
    return users, gender, oldest, youngest, common_bd, rentals_age

def print_data(df):
    
    """ Show raw data, five rows at the time """
    
    rows = df["Start Station"].count()
    span = 0
    while True:
        
        # Check if the next rows are the lastn, then show the last rows and do not give an option to continue
        if (span + 5) > rows:
            print(df.iloc[span:])
            print("You have reached the end of the data")
            break
        print(df.iloc[span:span+5])
        answer = input("Do you want to see another five rows of data? Enter Y to continue, any other key to stop showing data. ")
        if answer.lower() == "y":
            span += 5
        else:
            break
 

def main():
    while True:
        
        #df = load_data("Chicago", "June", "Monday")

        city, month_filter, weekday_filter = get_filters()

        df = load_data(city, month_filter, weekday_filter)

        hour, hour_rentals, day, day_rentals, month, month_rentals = time_stat(df)

        start_station, start_rentals, end_station, end_rentals, journey, journey_rentals = station_stat(df)

        trip_total, trip_mean = trip_duration(df)

        users, gender, oldest, youngest, common_bd, rentals_age = user_info(df, city)

        print()
        print("------------------------------------------------------------------------------------------------")
        print()
        print("Here is data about the selected city, day and month. Note that if you have filtered on a month or a day that month or day will be presented as the most popular one.")
        print()
        print("You have made the following selections, city is {}, month is {} and day is {}.".format(city, month_filter, weekday_filter))
        print()
        print("------------------------------------------------------------------------------------------------")
        print()
        print("Here is some data about when bikes are rented.")
        print()
        print ("The most popular hour is {}:00-{}:59 with {} number of rentals.".format(hour, hour, hour_rentals))
        print()
        print("The most popular day is {} with {} number of rentals.".format(day, day_rentals))
        print()
        print("The most popular month is {} with {} number of rentals.".format(month, month_rentals))
        print()
        print("------------------------------------------------------------------------------------------------")
        print()
        print("Some data about the stations beween which the bikes were used.")
        print()
        print("The most poular start station is {} where {} trips started.".format(start_station, start_rentals))
        print()
        print("The most poular end station is {} where {} trips ended.".format(end_station, end_rentals))
        print()
        print("The most poular end journey is from {} with {} trips.".format(journey, journey_rentals))
        print()
        print("------------------------------------------------------------------------------------------------")
        print()
        print("Some data about the trip durations")
        print()
        print("The total trip duration for all trips was {} minutes (about {} hours). The average trip duration was about {} minutes".format(math.trunc(trip_total/60), math.trunc(trip_total/3600),math.trunc(trip_mean/60)))
        print()
        print("------------------------------------------------------------------------------------------------")
        print()
        print("Some data about the users")
        print()
        print("This is the number of users within each user type")
        print()
        print(users.to_string())

        # User information is not available for Washington

        if city == "Washington":
            print()
            print("There is no more information about the users for Washington")
        else:    
            print()
            print("The number of users per gender")
            print()
            print(gender.to_string())
            print()
            print("The oldest user was born {} and the youngest user was born {}".format(math.trunc(oldest), math.trunc(youngest)))
            print()
            print("The most common birth year for those renting bikes was {} and customers born this year rented bikes {} times.".format(math.trunc(common_bd), rentals_age))

            
        print()
        print("------------------------------------------------------------------------------------------------")
        print()
        view_data = input("Do you want to view the raw data? (Y) or press any other button to contrinue without shoing the raw data? ")
        if view_data.lower() == "y":
            print_data(df)
        print("------------------------------------------------------------------------------------------------")
        restart = input("Do you want to restart (Y) or end (N): ")
        if restart.lower() != "y":
            break
            
if __name__ == "__main__":
    main()
