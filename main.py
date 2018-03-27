# Main.py
# Main program for charger
# IF curious why if name == main thing:
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do

import NoGui as nog
import support_lib as lib

# TODO: move to a config file that's not on git
# DONE: parameterize BatteryCharger
# TODO: parameterize ports, add linux/win detection to use right one
    # - this requuires redoing nogui for adjusting some config that uses defaults and maybe a user defined one that is in the .gitignore
# TODO: Feature: View the config? or at least notify the user where the profile/schedule is for some battery
#port = 'COM6'
# port = '/dev/ttyUSB0'
#port = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'

# Test ports with: python -m serial.tools.list_ports

if __name__ == "__main__":
    conf = lib.getConf()
    nog.startupNoGUI(conf['port']) 
    # print(conf)
    ''' Test of multi-layer modular code '''
