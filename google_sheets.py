import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEET_NAME

def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

def append_row(row_data):
    sheet = get_sheet()
    sheet.append_row(row_data)
    print(f"Добавлена строка: {row_data}")