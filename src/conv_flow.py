from typing import Dict, Any
import re
from .vapi import start_outbound_call, get_call_data
from .gsheets import log_call_data
from .email import send_confirmation_email

def extract_email_from_transcript(transcript: str) -> str:
    """
    tries to find an email address in the transcript using a simple regex
    returns the first email found or an empty string
    """
    # simple regex to match most emails
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    match = re.search(pattern, transcript)
    return match.group(0) if match else ""

def handle_outbound_receptionist(assistant_id: str) -> None:
    """
    orchestrates an outbound call to the user's phone
    logs call data and sends an email if found in the transcript
    """
    print('please enter your phone number in e.164 format (e.g. +91...)')
    user_phone = input('phone number: ').strip()

    call_id = start_outbound_call(assistant_id, user_phone)
    if not call_id:
        print('failed to start outbound call.')
        return

    print('call started. wait for the call to end, then we will fetch data...')

    # at this point, the user picks up, speaks to the assistant, then the call ends
    # we can prompt the user to press enter once the call is finished
    input('press enter after the call has ended on your phone... ')

    # now fetch post-call data
    call_data = get_call_data(call_id)
    print('call data retrieved:', call_data)

    # parse out an email from the transcript, if any
    transcript = call_data.get('transcript', '')
    found_email = extract_email_from_transcript(transcript)

    # log the call data to google sheets
    log_call_data({
        "call_id": call_data.get("call_id"),
        "status": call_data.get("call_status"),
        "ended_reason": call_data.get("ended_reason"),
        "duration": call_data.get("duration"),
        "transcript": transcript,
        "found_email": found_email
    })

    # if we found an email, send a confirmation
    if found_email:
        send_confirmation_email(found_email, "appointment details: 10 am tomorrow (example)")
        print('sent confirmation email to:', found_email)
    else:
        print('no email found in transcript, skipping email sending.')
    
    print('flow complete.')
