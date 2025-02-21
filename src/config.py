import os
from dotenv import load_dotenv

load_dotenv() 

VAPI_API_KEY = os.getenv('VAPI_API_KEY', '')
VAPI_BASE_URL = os.getenv('VAPI_BASE_URL', 'https://api.vapi.ai')

PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID', '')

GSHEET_SPREADSHEET_ID = os.getenv('GSHEET_SPREADSHEET_ID', '')
GSHEET_CREDENTIALS_FILE = os.getenv('GSHEET_CREDENTIALS_FILE', '')


EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
