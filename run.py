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

# WELCOME SECTION

def collect_welcome():
    # User provides correct data & type
    # While loop exits f if data is valid
    while True:
        welcome_selection = input("\nPlease select which task you would like to execute:\n \n 1. Update venue booking\n 2. Display previous entry\n 3. Display venue current booked seats\n 4. Display venue maximum seats\n \n")
        datas = welcome_selection

        if correct_welcome(datas):
            break

    return welcome_selection

def correct_welcome(datas):
    # Checks if data provided is correct
    # Try statement checks for correct number of data
    try:
        [str(data) for data in datas]
        if datas == "1":
            print(f"\nYou have selected {datas}")
        elif datas == "2":
            print(f"\nYou have selected {datas}")
        elif datas == "3":
            print(f"\nYou have selected {datas}")
        elif datas == "4":
            print(f"\nYou have selected {datas}")
        else:
            raise ValueError(
                f"ERROR: {datas} is not a valid entry. Please submit a value from 1 - 4")

    except ValueError as e:
        print(f"ERROR: {e}, Please try again\n")
        return False

    return True

# DATA INPUT SECTION

def collect_data():
    # User provides correct data & type
    # While loop exits f if data is valid
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

# DISPLAY f's SECTION

def display_row_values():
    # Display the specified row values and return a dictionary with venue names & booking amounts
    # last_row_updated = venues page last updated row (found by length of the column values)
    venues = SS.worksheet("venues").row_values(1)
    last_row_updated = SS.worksheet("venues").row_values(len(SS.worksheet("venues").col_values(1)))

def display_selection():
    # Input for what specific information user wants to display
    while True:
        display_option = input("\nPlease select which information you would like to view:\n \n 1. Last updated row\n 2. Last 5 updated rows\n 3. All spreadsheet values\n 4. Custom / Specific row\n \n")
        
        if correct_display_value():
            break

    return display_option

# UPDATE SECTION

def update_SS(next_row, worksheet):
    # Update the specified spreadsheet section, will be passed parameters in main()
    print(f"\nUpdating {SS}...\n")
    worksheet_to_update = SS.worksheet("venues")

    # Adds new row to the end of the current data
    worksheet_to_update.append_row(next_row)

    print(f"{SS} worksheet updated successfully\n")

# MAIN

def general_functions():

    # For all general program f's

    # Welcome section f's
    datas = collect_welcome()
    if datas == "1":
        # Data collection / validation f's
        seats = collect_data()
        seats_list = [int(i) for i in seats]

    # UPDATE f CALLING SECTION

    # Spreadsheet update function
    update_SS(seats_list, "VENUE-booker-ss")

# RUN PROGRAM

print("\nWelcome to VENUE booker!")
main = general_functions()

# TO CHECK ~~ Issue with gspread

#TOMORROW - CLEAN CODE // DISPLAY PREVIOUS BOOKINGS FUNCTION // SPICE UP CODE // NO LOOSE CODE // functions can call general functions lines
