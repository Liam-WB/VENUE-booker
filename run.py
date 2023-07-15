# Import library and credentials variable

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
    # If statement collects
    welcome_selection = input("\nPlease select which task you would like to execute:\n \n 1. Update a venue booking\n 2. Display venue maximum seats\n 3. Display venue current booked seats\n \n")
    if (welcome_selection == "1"):
        print(f"You have selected {welcome_selection}")
    elif (welcome_selection == "2"):
        print(f"You have selected {welcome_selection}")
    elif (welcome_selection == "3"):
        print(f"You have selected {welcome_selection}")
    else:
        print(f"ERROR: {welcome_selection} is not a valid entry. Please submit a value from 1 - 3.")
        return False

        # make function validate and rerun

def collect_data():
    # User provides correct data & type
    # While loop exits function  if data is valid
    while True:
        print("\nPlease provide the updated seats\nIn the format:\nX, X, X, X, X, X, X")
        seats_input = input("\nProvide the data below: \n\n")

        seats_list = list(seats_input.split(","))

        if correct_data(seats_list):
            break

    return seats_list

def correct_data(seats):
    # Checks if data provided is correct
    # Try statement checks for correct number of data
    try:
        [int(seat) for seat in seats]
        if len(seats) != 7:
            raise ValueError(
                f"A value for each of the 7 venues is required - You submitted {len(seats)} values.")

    except ValueError as e:
        print(f"ERROR: {e}, please try again\n")
        return False

    return True

def update_SS(next_row, worksheet):
    # Function update the specified spreadsheet section, will be passed parameters in the main() function
    print(f"Updating {SS}...\n")
    worksheet_to_update = SS.worksheet("venues")

    # adds new row to the end of the current data
    worksheet_to_update.append_row(next_row)

    print(f"{SS} worksheet updated successfully\n")


def general_functions():

    # For all general program functions
    welcome_data = welcome()

    seats = collect_data()
    seats_list = [int(i) for i in seats]

    update_SS(seats_list, "VENUE-booker-ss")
    # To add

# To add worksheet update functions

print("\nWelcome to VENUE booker!")

# lines to be added

welcome()