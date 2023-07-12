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
    welcome_selection = input("Welcome!\n Please select which task you would like to execute:\n 1. Update a venue booking\n 2. Display venue maximum seats\n 3. Display venue current booked seats\n")
    if (welcome_selection == 1):
        collect_data()
    elif (welcome_selection == 2):
        display_max_seats()
    elif (welcome_selection == 3):
        display_current_seats()
    else:
        return "ERROR: Please provide a valid entry"

def collect_data():

def display_max_seats():

def display_current_seats():