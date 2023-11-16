import gspread
from google.auth import load_credentials_from_file


def get_google_sheets_data(sheet_url, credentials_path):
    credentials, _ = load_credentials_from_file(credentials_path)
    gc = gspread.authorize(credentials)

    # Extract data from the Google Sheet
    worksheet = gc.open_by_url(sheet_url).sheet1
    data = worksheet.get_all_values()

    return data
