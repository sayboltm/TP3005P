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
    # - this is probably side effect of python text buffer with limited print
    # statements
    # in this prgrm
# TODO: add timestamp to output, investigate logging module. 
#       Need to root cause the serial disconnect.
# TODO: There is still the issue of device staying in remote mode after
# disconnect. This has been problem since Richard's original library.
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

# Handle whatever this is:
#Traceback (most recent call last):
#  File "main.py", line 22, in <module>
#    conf = lib.getConf()
#  File "C:\Users\Mike\GitHub\sayboltm\TP3005P\NoGui.py", line 87, in startupNoGUI
#    Bat.ChargeBattery()
#  File "C:\Users\Mike\GitHub\sayboltm\TP3005P\BatteryCharger.py", line 212, in ChargeBattery
#    amps = lib.amps_meas()
#  File "C:\Users\Mike\GitHub\sayboltm\TP3005P\TP3005P.py", line 137, in amps_meas
#    ser1.write(cmd)
#  File "C:\Users\Mike\Miniconda3\envs\spyderDev2\lib\site-packages\serial\serialwin32.py", line 315, in write
#    raise SerialException("WriteFile failed ({!r})".format(ctypes.WinError()))
#serial.serialutil.SerialException: WriteFile failed (PermissionError(13, 'The device does not recognize the command.', None, 22))

# happened randomly, I think the PSU disconnected or something, a beep/response
# from the machine when I think this occured was present. Almost got up to
# investigate. Should have. PSU kept on past the C/20 cutoff since the serial
# connection broke.
