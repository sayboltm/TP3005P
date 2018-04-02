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
# TODO: no alert anymore for changing from CC to CV mode?
#port = 'COM6'
# port = '/dev/ttyUSB0'
#port = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'

# Test ports with: python -m serial.tools.list_ports

if __name__ == "__main__":
    conf = lib.getConf()
    nog.startupNoGUI(conf['serial port']) 
#    print(conf)
    ''' Test of multi-layer modular code '''
# TODO handle typing wrong battery profile, triggers key error and quits
#TODO handle unplugged/wrong port
#Traceback (most recent call last):
#  File "main.py", line 22, in <module>
#    nog.startupNoGUI(conf['serial port'])
#  File "C:\Users\Mike\GitHub\sayboltm\TP3005P\NoGui.py", line 15, in startupNoGUI
#    lib.init_comm(port)
#  File "C:\Users\Mike\GitHub\sayboltm\TP3005P\TP3005P.py", line 45, in init_comm
#    ser1 = serial.Serial(port, 9600, timeout=1)
#  File "C:\Users\Mike\Miniconda3\envs\spyderDev2\lib\site-packages\serial\serialwin32.py", line 31, in __init__
#    super(Serial, self).__init__(*args, **kwargs)
#  File "C:\Users\Mike\Miniconda3\envs\spyderDev2\lib\site-packages\serial\serialutil.py", line 240, in __init__
#    self.open()
#  File "C:\Users\Mike\Miniconda3\envs\spyderDev2\lib\site-packages\serial\serialwin32.py", line 62, in open
#    raise SerialException("could not open port {!r}: {!r}".format(self.portstr, ctypes.WinError()))
#serial.serialutil.SerialException: could not open port 'COM6': FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)
