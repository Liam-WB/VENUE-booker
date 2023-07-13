# Imported library and credentials variable

import gspread
from google.oauth2.service_account import Credentials

# Global variables list - Defined in caps lock

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("credentials.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SS = GSPREAD_CLIENT.open("VENUE-booker-ss")

# TEMP CODE - Shows that api and Google sheet are connected

venues = SS.worksheet("venues")

venues_data = venues.get_all_values()

print(venues_data)

# NEXT - Add efficient functions, dict() method with zip() to create dictionaries for each page of SS

# TO CHECK vv // Issue with gspread?

def welcome():
    # Provide user with venue category option
    welcome_selection = input("Please select which task you would like to execute:\n 1. Update a venue booking\n 2. Display venue maximum seats\n 3. Display venue current booked seats\n")
    if (welcome_selection == 1):
        collect_data()
    elif (welcome_selection == 2):
        display_max_seats()
    elif (welcome_selection == 3):
        display_current_seats()
    else:
        raise ValueError(
                f"ERROR: {welcome_selection} is not a valid entry.")

def collect_data():
    # User provides correct data & type
    # While loop
    while True:
        print("Please provide the updated seats\n In the format:\n X, X, X, X, X, X, X, X, X")
        seats_input = input("Provide the data below: \n")

        seats_list = list(seats_input.split(","))

        if correct_seats(seats_list):
            break

    return seats_list

def correct_data(seats):
    # Checks if data provided is correct
    # Try statement checks for correct number of data
    try:
        [int(seat) for seat in seats]
        if len(values) != 9:
            raise ValueError(
                f"9 values are required - You submitted {len(seats)} values.")

    except ValueError as e:
        print(f"Invalid submission: {e}, please try again\n")
        return False

    return True


def general_functions():
    # For all general program functions
    seats = collect_data()
    seats_list = [int(i) for i in seats]
    # To add

# To add worksheet update functions

def display_max_seats(seats):
    # Display a dictionary containing venue & data lists
    venue_list = [x for x in SS.worksheet("VENUE-booker-ss").row_values(1)]
    sseats_dictionary = dict(zip(venue_list, seats))
    return seats_dictionary
    
    # To be changed
    stock_values = get_stock_values(stock_data)
    print(stock_values)
    

def display_current_seats():
    # To be added

print("Welcome to VENUE booker!")
# line to be added

