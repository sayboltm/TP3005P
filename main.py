# Main.py
# Main program for charger
# IF curious why if name == main thing:
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do

import NoGui as nog

# TODO: move to a config file that's not on git
#port = 'COM6'
port = '/dev/ttyUSB0'
#port = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'

# Test ports with: python -m serial.tools.list_ports

if __name__ == "__main__":
   nog.startupNoGUI(port) 
