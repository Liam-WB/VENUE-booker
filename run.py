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
    # While loop exits function  if data is valid
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
        if datas == "1" or "2" or "3" or "4":
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
    print(f"\nUpdating {SS}...\n")
    worksheet_to_update = SS.worksheet("venues")

    # adds new row to the end of the current data
    worksheet_to_update.append_row(next_row)

    print(f"{SS} worksheet updated successfully\n")

def general_functions():

    # For all general program functions

    # Welcome section functions
    datas = collect_welcome()
    if datas == "1":
        # Data collection / validation functions
        seats = collect_data()
        seats_list = [int(i) for i in seats]

    # Spreadsheet update function
    update_SS(seats_list, "VENUE-booker-ss")

    # To add

print("\nWelcome to VENUE booker!")
main = general_functions()

# TO CHECK vv // Issue with gspread

#TOMORROW - CLEAN CODE // DISPLAY PREVIOUS BOOKINGS FUNCTION // SPICE UP CODE // NO LOOSE CODE // functions can call general functions lines