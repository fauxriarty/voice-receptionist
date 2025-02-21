import re
from typing import Dict, Any, Tuple
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

    call_id, start_debug = start_outbound_call(assistant_id, user_phone)
    if not call_id:
        # call creation failed; log partial data
        data_to_log = {
            "Call ID": "none",
            "Status": "failed to start",
            "Reason Ended": "n/a",
            "Duration": "0",
            "Transcript": "",
            "Found Email": "",
            "Debug Info": start_debug
        }
        log_call_data(data_to_log)
        return

    print("call started. wait for the call to complete, then press enter...")
    input("press enter after the call has ended on your phone...")

    # fetch call data
    call_data, get_debug = get_call_data(call_id)
    transcript = call_data.get("transcript", "")
    found_email = extract_email_from_transcript(transcript)

    # combine the debug logs
    combined_debug_log = (
        "--- start outbound call debug ---\n"
        f"{start_debug}\n\n"
        "--- get call data debug ---\n"
        f"{get_debug}"
    )

    data_to_log = {
        "Call ID": call_data.get("call_id", ""),
        "Status": call_data.get("call_status", ""),
        "Reason Ended": call_data.get("ended_reason", ""),
        "Duration": str(call_data.get("duration", 0)),
        "Transcript": transcript,
        "Found Email": found_email,
        "Debug Info": combined_debug_log
    }

    log_call_data(data_to_log)

    if found_email:
        send_confirmation_email(found_email, "appointment details: 10 am tomorrow (example)")
        print("sent confirmation email to:", found_email)
    else:
        print("no email found in transcript, skipping email sending.")

    print("flow complete.")
