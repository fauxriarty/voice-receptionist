import re
from typing import Dict, Any
from .vapi import start_outbound_call, get_call_data
from .gsheets import log_call_data
from .email import send_confirmation_email

def extract_email_from_transcript(transcript: str) -> str:
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(pattern, transcript)
    return match.group(0) if match else ""

def handle_outbound_receptionist(assistant_id: str) -> None:
    print("please enter your phone number in e.164 format (e.g. +91...):")
    user_phone = input("phone number: ").strip()

    # start call
    call_id, start_debug = start_outbound_call(assistant_id, user_phone)
    if not call_id:
        print("failed to start outbound call.")
        # we can log the debug info to google sheets if you want
        debug_data = {
            "call_id": "none",
            "status": "failed to start",
            "debug_log": start_debug
        }
        log_call_data(debug_data)
        return

    print("call started. wait for the call to complete, then press enter...")
    input("press enter after the call has ended on your phone...")

    # fetch call data
    call_data, get_debug = get_call_data(call_id)
    transcript = call_data.get("transcript", "")
    found_email = extract_email_from_transcript(transcript)

    # build a single debug log string
    combined_debug_log = f"--- start outbound call debug ---\n{start_debug}\n\n--- get call data debug ---\n{get_debug}"

    # we store all relevant data in one dict
    # so you can see everything in the sheet
    data_to_log = {
        "call_id": call_data.get("call_id", ""),
        "call_status": call_data.get("call_status", ""),
        "ended_reason": call_data.get("ended_reason", ""),
        "duration": call_data.get("duration", ""),
        "transcript": transcript,
        "found_email": found_email,
        "debug_log": combined_debug_log
    }

    # log to google sheets
    log_call_data(data_to_log)

    # if we found an email, send a confirmation
    if found_email:
        send_confirmation_email(found_email, "appointment details: 10 am tomorrow (example)")
        print("sent confirmation email to:", found_email)
    else:
        print("no email found in transcript, skipping email sending.")

    print("flow complete.")
