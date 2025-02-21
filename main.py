from src.conv_flow import handle_outbound_receptionist
from src.vapi import start_outbound_call, get_call_data

def main() -> None:
    print("welcome to the voice ai receptionist testing system.")
    print("choose an option:")
    print("1. run full conversation flow (outbound call)")
    print("2. get call data for a call id (just debug fetch)")

    option = input("enter option (1/2): ").strip()
    
    if option == "1":
        assistant_id = input("enter your assistant id: ").strip()
        handle_outbound_receptionist(assistant_id)
    elif option == "2":
        call_id = input("enter call id to fetch data: ").strip()
        call_data, debug_log = get_call_data(call_id)
        print("call data retrieved:", call_data)
        print("\n--- debug log ---\n", debug_log)
    else:
        print("invalid option, exiting.")

if __name__ == "__main__":
    main()
