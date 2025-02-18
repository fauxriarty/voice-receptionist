from src import vapi

def main() -> None:
    print('testing vapi integration functions')
    # since you're creating the assistant manually, provide its id here
    assistant_id = input('enter your manually created assistant id: ').strip()
    
    print('choose an option:')
    print('1. start inbound call')
    print('2. get call data')
    option = input('enter option (1/2): ').strip()

    if option == '1':
        caller_id = input('enter caller id (phone number): ')
        call_id = vapi.start_inbound_call(assistant_id, caller_id)
        if call_id:
            print('inbound call started, call id:', call_id)
        else:
            print('failed to start inbound call')
    elif option == '2':
        call_id = input('enter call id to fetch data: ')
        data = vapi.get_call_data(call_id)
        print('call data retrieved:')
        for key, value in data.items():
            print(f'{key}: {value}')
    else:
        print('invalid option, exiting')

if __name__ == '__main__':
    main()
