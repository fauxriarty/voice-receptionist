import re
from typing import Dict, Any, Tuple
from .vapi import start_outbound_call, get_call_data
from .gsheets import log_call_data
from .email import send_confirmation_email

def parse_spelled_out_email(transcript: str) -> str:
    # based on practice webcalls where userinput gets logged as dot, at , g mail, etc
    replaced = transcript.lower()
    replaced = replaced.replace("'", "")
    replaced = replaced.replace(",", "")
    replaced = replaced.replace(" dot ", ".")
    replaced = replaced.replace(" at ", "@")
    replaced = replaced.replace("g mail", "gmail")

    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    match = re.search(pattern, replaced)
    return match.group(0) if match else ""

def handle_outbound_receptionist(assistant_id: str) -> None:
    print("please enter your phone number in e.164 format (e.g. +91...):")
    user_phone = input("phone number: ").strip()

    call_id, start_debug = start_outbound_call(assistant_id, user_phone)
    if not call_id:
        data_to_log = {
            "Call ID": "none",
            "Status": "failed to start",
            "Reason Ended": "n/a",
            "Duration": "0",
            "Transcript": "",
            "Found Email": "",
            "Start Time": "",
            "End Time": "",
            "Recording URL": "",
            "Call Summary": "",
            "Cost": "",
            "Debug Info": start_debug
        }
        log_call_data(data_to_log)
        return

    print("call started. wait for the call to complete, then press enter...")
    input("press enter after the call has ended on your phone...")

    call_data, get_debug = get_call_data(call_id)
    found_email = parse_spelled_out_email(call_data.get("transcript", ""))

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
        "Transcript": call_data.get("transcript", ""),
        "Found Email": found_email,
        "Start Time": call_data.get("started_at", ""),
        "End Time": call_data.get("ended_at", ""),
        "Recording URL": call_data.get("recording_url", ""),
        "Call Summary": call_data.get("analysis_summary", ""),
        "Cost": str(call_data.get("cost", 0)),
        "Debug Info": combined_debug_log
    }

    log_call_data(data_to_log)

    if found_email:
        send_confirmation_email(found_email, "appointment details: 10 am tomorrow (example)")
        print("sent confirmation email to:", found_email)
    else:
        print("no email found in transcript, skipping email sending.")

    print("flow complete.")
