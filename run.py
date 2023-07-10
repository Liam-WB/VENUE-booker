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

large_venues = SS.worksheet("large_venues")

large_venues_data = large_venues.get_all_values()

print(large_venues_data)

# NEXT - Add efficient functions, dict() method with zip() to create dictionaries for each page of SS