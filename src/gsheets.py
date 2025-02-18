from typing import Dict, Any
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .config import GSHEET_SPREADSHEET_ID, GSHEET_CREDENTIALS_FILE

def get_sheets_service():
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(
        GSHEET_CREDENTIALS_FILE,
        scopes=scopes
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def log_call_data(call_data: Dict[str, Any]) -> None:
    """
    appends call_data to the google sheet.
    each dictionary key becomes a column in the appended row.
    """
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        # for consistent ordering, let's sort the keys
        row_values = []
        for key in sorted(call_data.keys()):
            row_values.append(str(call_data[key]))

        body = {"values": [row_values]}
        sheet.values().append(
            spreadsheetId=GSHEET_SPREADSHEET_ID,
            range='Sheet1!A1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        print('logged call data to google sheets')
    except Exception as e:
        print('error logging to google sheets:', e)
