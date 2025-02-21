from typing import Dict, Any
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .config import GSHEET_SPREADSHEET_ID, GSHEET_CREDENTIALS_FILE

def get_sheets_service():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = service_account.Credentials.from_service_account_file(
        GSHEET_CREDENTIALS_FILE, scopes=scopes
    )
    service = build("sheets", "v4", credentials=credentials)
    return service

def log_call_data(call_data: Dict[str, Any]) -> None:
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()

        # define a fixed column order for 12 columns
        column_order = [
            "Call ID",
            "Status",
            "Reason Ended",
            "Duration",
            "Transcript",
            "Found Email",
            "Start Time",
            "End Time",
            "Recording URL",
            "Call Summary",
            "Cost",
            "Debug Info"
        ]

        # build row in that exact order
        row_values = []
        for col in column_order:
            row_values.append(str(call_data.get(col, "")))

        body = {"values": [row_values]}
        sheet.values().append(
            spreadsheetId=GSHEET_SPREADSHEET_ID,
            range="Sheet1!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        print("logged call data to google sheets")
    except Exception as e:
        print("error logging to google sheets:", e)
