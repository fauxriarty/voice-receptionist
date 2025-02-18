# main.py
from src import conv_flow

def main() -> None:
    print('welcome to the voice ai receptionist system.')
    assistant_id = input('please enter your assistant id: ').strip()
    conv_flow.handle_outbound_receptionist(assistant_id)

if __name__ == '__main__':
    main()
