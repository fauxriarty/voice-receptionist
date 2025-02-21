# Voice AI Receptionist

This project implements a Voice AI Receptionist using Vapi for voice call interactions, the Google Sheets API for real‐time logging of call data, and Python’s smtplib for sending email confirmations. The assistant simulates appointment booking by managing calls, extracting relevant details from call transcripts, and logging all call information in a structured format.

## Overview

The solution integrates:
- **Vapi API**: To initiate outbound calls and retrieve call data (transcripts, call status, start/end times, cost, etc.).
- **Google Sheets API**: To log call data in a structured manner with fixed columns (Call ID, Status, Reason Ended, Duration, Transcript, Found Email, Start Time, End Time, Recording URL, Call Summary, Cost, Debug Info).
- **Email Notification**: Using Gmail (via smtplib) to send confirmation emails if an email address is detected in the transcript.
- **Debug Logging**: Detailed debug logs are captured and stored to assist with troubleshooting and demonstration.

## Project Structure

voice-receptionist/
├── .env
├── README.md
├── requirements.txt
└── src/
    ├── init.py
    ├── config.py
    ├── vapi.py
    ├── gsheets.py
    ├── email.py
    ├── conv_flow.py
    └── main.py

- **config.py**  
  Loads all configuration variables (Vapi API keys, phone number id, Google Sheets credentials, email credentials) from the `.env` file.

- **vapi.py**  
  Contains functions to initiate outbound calls and fetch call details from Vapi. It also calculates the call duration by parsing the `startedAt` and `endedAt` fields.

- **gsheets.py**  
  Connects to Google Sheets using a service account and appends call data in a fixed column order.

- **email.py**  
  Uses Python’s smtplib to send email confirmations. It is designed to work with Gmail; note that you must use an app password if 2-step verification is enabled.

- **conv_flow.py**  
  Implements the overall conversation flow. It triggers a call, waits for it to complete, fetches call data, extracts an email address from the transcript (using advanced parsing for spoken-out email addresses), and logs all details to Google Sheets.

- **main.py**  
  Provides an interactive terminal interface to run either the full conversation flow or simply fetch call data (by providing a call id).

## Vapi API Integration

- **Endpoints used**:
  - POST /call: Initiates an outbound call. The payload includes:
    - type: "outboundPhoneCall"
    - assistantId: the Vapi assistant ID (created via the dashboard)
    - phoneNumberId: the ID of the Vapi phone number configured for outbound calls
    - customer.number: the recipient’s phone number in e.164 format.
  - GET /call/{call_id}: Retrieves details for a given call. From the response, the code extracts:
    - status
    - endedReason
    - startedAt and endedAt (used to compute call duration)
    - artifact.transcript
    - analysis.summary
    - artifact.recordingUrl
    - cost
- The call duration is computed by parsing the ISO8601 timestamps from startedAt and endedAt.

## Google Sheets Logging

The project uses the Google Sheets API (via a service account) to append call data. The data is logged with the following fixed columns:
1. Call ID
2. Status
3. Reason Ended
4. Duration
5. Transcript
6. Found Email
7. Start Time
8. End Time
9. Recording URL
10. Call Summary
11. Cost
12. Debug Info

Ensure your Google Sheet is shared with the service account email (configured via the service account JSON key file path in the .env file).

## Email Notification System

Uses Gmail’s SMTP server at smtp.gmail.com (port 587) to send confirmation emails. You must set your EMAIL_USER and generate an app password (without spaces) if 2-step verification is enabled. The system attempts to extract a valid email from the call's transcript or analysis summary by converting spoken-out email components (e.g. “dot”, “at”, “g mail”) into standard email format.

## Debug Logging

Both the call initiation and data retrieval functions in vapi.py capture debug logs (e.g. payload, response status, truncated response text). These debug logs are combined and stored in the “Debug Info” column in Google Sheets to help diagnose any issues.

## API Endpoints Used

Vapi API:
- POST /call: Initiates a call.
- GET /call/{call_id}: Retrieves call details.

Google Sheets API:
- spreadsheets.values.append: Appends a row to your spreadsheet.

SMTP (Gmail):
- Gmail’s SMTP server is used to send confirmation emails.


## Setup Instructions

1. Clone the Repository  
   ```bash
   git clone <repository_url>
   cd voice-receptionist
   ```

2. Create and Activate a Virtual Environment  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # linux/mac
   venv\Scripts\activate       # windows
   ```

3. Install Dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment Variables  
   Create a .env file in the project root with the following (replace placeholder values with your actual credentials):
   ```
   VAPI_API_KEY=your_vapi_api_key
   VAPI_BASE_URL=https://api.vapi.ai
   PHONE_NUMBER_ID=your_vapi_phone_number_id

   GSHEET_SPREADSHEET_ID=your_google_sheet_id
   GSHEET_CREDENTIALS_FILE=/absolute/path/to/your_service_account_credentials.json

   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

   Google Sheets: Enable the Google Sheets API via the Google Cloud Console, create a service account, download the JSON key file, and share your spreadsheet with the service account email.

   Email: If you use Gmail, generate an app password (without spaces) from your Google Account's security settings.

## Running the Project

Run the project using:
```bash
python3 main.py
```


