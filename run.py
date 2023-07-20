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
        welcome_selection = input("\nPlease select which task you would like to execute:\n \n 1. Update venue booking\n 2. Display a previous entry\n 3. Display an entry's remaining seats\n 4. Display venue average booking amounts\n \n")
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
                f"{datas} is not a valid entry. Please submit a value from 1 - 4")

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

def collect_display():
    # Input for what specific (validated) information user wants to display
    while True:
        display_option = input("\nPlease select which booking(s) you would like to view:\n \n 1. Last updated row\n 2. Last 5 updated rows\n 3. All spreadsheet values\n 4. Custom / Specific row\n \n")
        display = display_option

        if correct_display(display):
            break

    return display_option

def correct_display(display):
    try:
        if display == "1":
            print(f"\nDisplaying last submitted data...\n")
        elif display == "2":
            print(f"\nDisplaying last 5 submissions in order of most recent...\n")
        elif display == "3":
            print(f"\nDisplaying all spreadsheet data...\n")
        elif display == "4":
            print(f"\nYou have selected a specific booking row:\n")
        else:
            raise ValueError(
                f"{display} is not a valid entry. Please submit a value from 1 - 4")

    except ValueError as e:
        print(f"ERROR: {e}, Please try again\n")
        return False

    return True

def display_row_values(display, worksheet):
    # Display the specified row values and return a dictionary with venue names & booking amounts
    # last_row_updated = venues page last updated row (found by length of the column values)

    # VARIABLES
    # Call SS row numbers
    last_row_updated = SS.worksheet(worksheet).row_values(len(SS.worksheet(worksheet).col_values(1)))
    second_row_updated = SS.worksheet(worksheet).row_values((len(SS.worksheet(worksheet).col_values(1))-1))
    third_row_updated = SS.worksheet(worksheet).row_values((len(SS.worksheet(worksheet).col_values(1))-2))
    fourth_row_updated = SS.worksheet(worksheet).row_values((len(SS.worksheet(worksheet).col_values(1))-3))
    fifth_row_updated = SS.worksheet(worksheet).row_values((len(SS.worksheet(worksheet).col_values(1))-4))
    headings = SS.worksheet(worksheet).row_values(1)
    # Create dictionary from row variables and venue names (using zip method)
    last_dict = dict(zip(headings, last_row_updated))
    second_dict = dict(zip(headings, second_row_updated))
    third_dict = dict(zip(headings, third_row_updated))
    fourth_dict = dict(zip(headings, fourth_row_updated))
    fifth_dict = dict(zip(headings, fifth_row_updated))

    # If statement dictates what data/variable is displayed
    if display == "1":
        return last_dict
    elif display == "2":
        return f"\n{last_dict}\n{second_dict}\n{third_dict}\n{fourth_dict}\n{fifth_dict}"
    elif display == "3":
        # For loop loops through rows number in SS and creates a dictionary for each item, linked to "headings" variable
        rows = SS.worksheet("venues").get_all_values()
        for row in rows:
            all = dict(zip(headings, row))
        return all

def collect_custom(worksheet):
    # Input for what specific (validated) information user wants to display
    while True:
        custom_option = input("\nPlease input a number of row which you would like to view:\n \n")
        custom = custom_option

        if correct_custom(custom, worksheet):
            break

    return custom_option

def correct_custom(custom, worksheet):
    rows = SS.worksheet(worksheet).get_all_values()
    valid_rows = [row for row in rows]
    try:
        if custom in valid_rows:
            raise ValueError(
                f"{custom} is not a valid row number from {worksheet}")
        else:
            print("Displaying selected data...")

    except ValueError as e:
        print(f"ERROR: {e}, Please try again\n")
        return False

    return True

# REMAINING SECTION

def calculate_remaining(display):
    keys = display_row_values(display, "venues")
    # Create list of only integers
    print("Creating data list...\n")
    keys_list = [i for i in keys.values()]
    # Calculate remaining seats
    print("\nCalculating remaining seats...\n")
    # Convert list items to int
    max_seats = [int(i) for i in SS.worksheet("remaining_seats").row_values(2)]
    keys_list = [int(i) for i in keys_list]
    headings = SS.worksheet("remaining_seats").row_values(1)
    remaining_seats = []
    for i, j in zip(max_seats, keys_list):
        remaining_seats.append(i - j)
    remaining_final = dict(zip(headings, remaining_seats))
    print(remaining_final)

# UPDATE SECTION

def update_SS(next_row, worksheet):
    # Update the specified spreadsheet section, will be passed parameters in main()
    print(f"\nUpdating {SS}...\n")
    worksheet_to_update = SS.worksheet(worksheet)

    # Adds new row to the end of the current data
    worksheet_to_update.append_row(next_row)

    print(f"{SS} worksheet updated successfully\n")

# MAIN

def general_functions():

    # MAIN

    # WELCOME f SECTION
    datas = collect_welcome()
    if datas == "1":
        # Data collection / validation f's
        seats = collect_data()
        seats_list = [int(i) for i in seats]
        # UPDATE f CALLING SECTION
        # Spreadsheet update function
        update_SS(seats_list, "venues")
    elif datas == "2" or "3" or "4":
        # DISPLAY f SECTION
        display = collect_display()

    if datas == "2":
        print(display_row_values(display, "venues"))
        if display == "4":
            custom = collect_custom("venues")
            print(dict(zip(SS.worksheet("venues").row_values(1), SS.worksheet("venues").row_values(custom))))
    elif datas == "3":
        remaining_final = calculate_remaining(display)

    #    if display == "4":
    #        custom = collect_custom("venues")
    #        print(dict(zip(SS.worksheet("venues").row_values(1), SS.worksheet("venues").row_values(custom))))

# RUN PROGRAM

print("\nWelcome to VENUE booker!")
main = general_functions()

# TO CHECK ~~ Issue with gspread

#TOMORROW - CLEAN CODE // DISPLAY PREVIOUS BOOKINGS FUNCTION // SPICE UP CODE // NO LOOSE CODE // functions can call general functions lines