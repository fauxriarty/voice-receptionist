import re
from src.vapi import get_call_data
from src.gsheets import log_call_data
from src.email import send_confirmation_email
from src.conv_flow import handle_outbound_receptionist, parse_spelled_out_email


def main() -> None:
    print("welcome to the voice ai receptionist testing system.")
    print("choose an option:")
    print("1. run full conversation flow (outbound call)")
    print("2. get call data for a call id (just debug fetch & log to sheets)")

    option = input("enter option (1/2): ").strip()
    
    if option == "1":
        assistant_id = input("enter your assistant id: ").strip()
        handle_outbound_receptionist(assistant_id)

    elif option == "2":
        call_id = input("enter call id to fetch data: ").strip()
        call_data, debug_log = get_call_data(call_id)

        found_email = parse_spelled_out_email(call_data.get("transcript", ""))

        combined_debug_log = f"--- get call data debug ---\n{debug_log}"

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

        print("call data retrieved and logged to sheets.")

    else:
        print("invalid option, exiting.")

if __name__ == "__main__":
    main()
