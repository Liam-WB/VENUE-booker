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
            print(f"\nYou have selected a specific booking row...\n")
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
        return last_dict, second_dict, third_dict, fourth_dict, fifth_dict
    elif display == "3":
        # For loop loops through rows number in SS and creates a dictionary for each item, linked to "headings" variable
        # Add \n format
        rows = SS.worksheet("venues").get_all_values()
        rows.pop(0)
        all = []
        for row in rows:
            all.append(dict(zip(headings, row)))
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
            print("\nDisplaying selected data...\n")

    except ValueError as e:
        print(f"ERROR: {e}, Please try again\n")
        return False

    return True

# REMAINING SECTION

def calculate_remaining(display):
    if display == "1":
        keys = display_row_values(display, "venues")
        # Create list of only integers
        print("Creating data list...\n")
        keys_list = list(keys.values()) 
        # Calculate remaining seats
        print("Calculating remaining seats...\n")
        # Convert list items to int
        max_seats = [int(i) for i in SS.worksheet("remaining_seats").row_values(2)]
        keys_list = [int(i) for i in keys_list]
        headings = SS.worksheet("remaining_seats").row_values(1)
        remaining_seats = []
        for i, j in zip(max_seats, keys_list):
            remaining_seats.append(i - j)
        remaining_final = dict(zip(headings, remaining_seats))
        return remaining_final
    elif display == "2":
        # Step by step copy of above process
        # **Could create function for efficient remaining seats calculation process for multiple data rows
        a, b, c, d, e = display_row_values(display, "venues")
        a = [int(val) for val in a.values()]
        b = [int(val) for val in b.values()]
        c = [int(val) for val in c.values()]
        d = [int(val) for val in d.values()]
        e = [int(val) for val in e.values()]
        keys_list = a,b,c,d,e
        # Create list of only integers
        print("Creating data list...\n")
        # Calculate remaining seats
        print("Calculating remaining seats...\n")
        # Convert list items to int
        max_seats = [int(i) for i in SS.worksheet("remaining_seats").row_values(2)]
        headings = SS.worksheet("remaining_seats").row_values(1)
        remaining_a = []
        remaining_b = []
        remaining_c = []
        remaining_d = []
        remaining_e = []
        for i, j in zip(max_seats, a):
            remaining_a.append(i - j)
        for i, j in zip(max_seats, b):
            remaining_b.append(i - j)
        for i, j in zip(max_seats, c):
            remaining_c.append(i - j)
        for i, j in zip(max_seats, d):
            remaining_d.append(i - j)
        for i, j in zip(max_seats, e):
            remaining_e.append(i - j)
        final_a = dict(zip(headings, remaining_a))
        final_b = dict(zip(headings, remaining_b))
        final_c = dict(zip(headings, remaining_c))
        final_d = dict(zip(headings, remaining_d))
        final_e = dict(zip(headings, remaining_e))
        remaining_final = final_a, final_b, final_c, final_d, final_e
        return remaining_final
    elif display == "3":
        # For loop loops through rows number in SS and creates a dictionary for each item, linked to "headings" variable
        rows = SS.worksheet("remaining_seats").get_all_values()
        headings = SS.worksheet("remaining_seats").row_values(1)
        rows.pop(0)
        all = []
        for row in rows:
            all.append(dict(zip(headings, row)))
        return all

# UPDATE SECTION

def update_SS(next_row, worksheet):
    # Update the specified spreadsheet section, will be passed parameters in main()
    print(f"\nUpdating {SS}...\n")
    worksheet_to_update = SS.worksheet(worksheet)

    # Adds new row to the end of the current data
    worksheet_to_update.append_row(next_row)

    print(f"{SS} worksheet updated successfully\n")

def update_remaining(next_row, worksheet):
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
        # Spreadsheet update f
        update_SS(seats_list, "venues")
        # Remaining seats update f
        max_seats = [int(i) for i in SS.worksheet("remaining_seats").row_values(2)]
        headings = SS.worksheet("remaining_seats").row_values(1)
        remaining_seats = []
        for i, j in zip(max_seats, seats_list):
            remaining_seats.append(i - j)
        update_remaining(remaining_seats, "remaining_seats")
    elif datas == "2" or "3":
        # DISPLAY f SECTION
        display = collect_display()
        if datas == "2":
            displayed = display_row_values(display, "venues")
            if displayed != None:
                print(displayed)
            if display == "4":
                custom = collect_custom("venues")
                print(dict(zip(SS.worksheet("venues").row_values(1), SS.worksheet("venues").row_values(custom))))
        elif datas == "3":
            if display == "1" or "2" or "3":
                remaining_final = calculate_remaining(display)
                print(remaining_final)
            if display == "4":
                custom = collect_custom("remaining_seats")
                print(dict(zip(SS.worksheet("remaining_seats").row_values(1), SS.worksheet("remaining_seats").row_values(custom))))

# RUN PROGRAM
print("\nWelcome to VENUE booker!")
main = general_functions()

# TO CHECK ~~ Issue with gspread
# SPICE UP CODE // NO LOOSE CODE
# NONE POPPING UP WHEN TYPE TOO FAST, 2, 4, specific