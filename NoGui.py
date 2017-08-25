# nogui library
# Eventually this program will have a GUI for ease of use of non programmers, but QT is a pain, and a backup nogui CLI design with a while loop needs to be used. Also easier to debug quickly.

import sys
import TP3005P as lib
import BatteryCharger as Bat

#### User Params ####
#port = 'COM6'
#port = 'ttyS31'
#####################


def startupNoGUI(port):
    lib.init_comm(port)
    # TODO: Fix error #1 caused by init comms when psu is off
    while True:
        print("Options:\n0 = quit\n1 = test PS function\n2=testCharger")
        mode = input("Select one.\n")

        # Check to make sure user is not stupid and entered a char of type INT
        try:
            mode = int(mode)
        except Exception as e:
                print('[-] SHTF.')
                #raise # What does this do? test when code copied into next program!
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                #print(exc_type, fname, exc_tb.tb_lineno) # why this not conv to str?
                print('[-] Exception Caught.\nType: ' + str(exc_type) + '\nText: ' 
                    + str(e) + '\nLine: ' + str(exc_tb.tb_lineno) + '\nIn file: ' 
                    + str(fname))
                sys.exit(10)
                       

        if mode == 0:
            lib.end_comm()
            break
        elif mode == 1:
            print('TestPSU')
            lib.test(port)
        elif mode == 2:
            print('Test charging function launch (not rly)')
        elif mode == 3:
            print('Test Voltage Set')
            volts = input('Set volts:\n')
            lib.volts_setpoint_set(float(volts))
            # TODO: clean all these inputs
        elif mode == 4:
            print('Test current set')
            amps = input('set amps:\n')
            lib.amps_setpoint_set(float(amps))
        elif mode == 5:
            print('status get')
            status = lib.status_get()
            print('Status: ' + str(status))
        elif mode == 6:
            print('amps_meas')
            amps = lib.amps_meas()
            print('amps: ' + str(amps))
        elif mode == 7:
            print ('vmeas')
            volts = lib.volts_meas()
            print('volts: ' + str(volts))
        elif mode == 8:
            print('basic comparison\nIf volts=8.2 and amps = 0.1, print agree.')
            amps = lib.amps_meas()
            volts = lib.volts_meas()
            vsetpt = lib.volts_setpoint_get()
            asetpt = lib.amps_setpoint_get()

            if (volts == 8.2) and (amps <= 0.1):
                print('Agree!')
                lib.output_state(0)
                print('Charging cycle complete!')
            else:
                print('Disagree.\nVolts: ' + str(volts) + '\nAmps: ' +
                        str(amps) + 'vset: ' + str(vsetpt) +'\nasetpt: ' +
                        str(asetpt))

        elif mode == 9:
            print('output state, 0 for off, 1 for on')
            state = input('O or 1:')
            lib.output_state(int(state))
        elif mode == 10:
            print('Running Charger!')
            Bat.ChargeBattery()
            break

        else:
            print('Invalid input! Redo.')


