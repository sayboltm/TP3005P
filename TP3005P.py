# Circumflex Designs 2017
#
#   init_comm(port_name)        Opens named com port and initializes comm
#   end_comm()                  Closes comm port
#
#   output_state(out_on)        If state is < 1 then output is turned off.  Otherwise, it is turned on.
#
#   volts_setpoint_set(volts)   Sets output voltage to volts
#   volts_setpoint_get()        Returns voltage setpoint from power supply
#   volts_meas()                Returns the output voltage measurement from the power supply
#
#   amps_setpoint_set(amps)     Sets output current (limit) to amps
#   volts_setpoint_get()        Returns current setpoint from power supply
#   volts_meas()                Returns the output current measurement from the power supply
#
#   status_get()                Returns the power supply status flags
#

import serial
import time
import sys
import os

######################
### User Params:
#port = 'COM6'
#port = 'ttyS31'
#####################
#Create the global serial object
ser1 = serial.Serial()


#Time delay - should instead use time.sleep()
def delay(secs):
    start = time.time()
    while ((time.time() - start) < secs):
        continue



#Initiate comm with PS
def init_comm(port):
    # Richard chose 'implicit serial declaration' where the object is implicitly referenced in background
    # compare this to sayboltm/CSCAN explicit serial archetecture where serial object is returned and referenced. Not sure of pros/cons
    global ser1

    ser1 = serial.Serial(port, 9600, timeout=1)
    print(ser1.name)
#    print ("Serial Port is Open: %d\n" % ser1.is_open)
    ser1.reset_input_buffer()
    ser1.reset_output_buffer()
    time.sleep(1)
    print (status_get())
    time.sleep(0.1)

def end_comm():
    ser1.close()


def output_state(out_on):
    time.sleep(0.05)
    if out_on >= 1:
        cmd = b'OUTPUT1:\\r\\n'
        print("Output On")
    else:
        cmd = b'OUTPUT0\\r\\n'
        print ("Output Off")
    ser1.write(cmd)
    #print (cmd)
    #print (out_on)
    time.sleep(0.05)


def volts_setpoint_set(volts):
    time.sleep(0.05)
    cmd = b'VSET1:'                      #b'VSET1:07.00\\r\\n'
    cmd = cmd + format(volts, "=05.2F").encode('ascii')
    cmd = cmd + b'\\r\\n'
    ser1.write(cmd)
    #print(cmd)

def volts_setpoint_get():
    time.sleep(0.05)
    cmd = b'VSET1?\\r\\n'
    ser1.write(cmd)
    line = ser1.readline()
    #print("Response: %s" % line)
    volts = float(line.decode('utf8'))
    return volts

def volts_meas():
    time.sleep(0.05)
    cmd = b'VOUT1?\\r\\n'
    ser1.write(cmd)
    line = ser1.readline()
    #print("Response: %s" % line)

    try:
        volts = float(line.decode('utf8'))
        return volts
    except ValueError:
        # Adding this in case it is failing printing te exception lol
        # Yes, this is exactly what is happening! UnboundLocalError exc_type
        # ref before assignment
        print('[-] [-] Badness > 9000! SHTF.')
        # does order matter? was that like else, then elif and not caught lol
        print('[-] Known exception Caught.\nType: ' + str(exc_type) + '\nText: ' 
            + str(e) + '\nLine: ' + str(exc_tb.tb_lineno) + '\nIn file: ' 
            + str(fname))
        print('Raw message from device: ' + line)
        sys.exit(10)
        # WHY THE HELL will this not catch the ValueError when weird shit comes
        # over the line???
#    finally:

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

def amps_setpoint_set(amps):
    time.sleep(0.05)
    cmd = b'ISET1:'                      #b'ISET1:2.500\\r\\n'
    cmd = cmd + format(amps, "=05.3F").encode('ascii')
    cmd = cmd + b'\\r\\n'
    ser1.write(cmd)
    #print(cmd)

def amps_setpoint_get():
    time.sleep(0.05)
    cmd = b'ISET1?\\r\\n'
    ser1.write(cmd)
    line = ser1.readline()
    #print("Response: %s" % line)
    amps = float(line.decode('utf8'))
    return amps

def amps_meas():
    time.sleep(0.05)
    cmd = b'IOUT1?\\r\\n'
    ser1.write(cmd)
    line = ser1.readline()
    #print("Response: %s" % line)
    amps = float(line.decode('utf8'))
    return amps


def status_get():
    time.sleep(0.05)
    cmd = b'STATUS?\\r\\n'
    ser1.write(cmd)
    line = ser1.readline()
    #print("Response: %s" % line)
    try:
        status = int(line.decode('utf8')) # TODO: Fails if off.. but isn't
        # caught by ValueError for some reason
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
    except ValueError:
        print('[-] Known exception Caught.\nType: ' + str(exc_type) + '\nText: ' 
            + str(e) + '\nLine: ' + str(exc_tb.tb_lineno) + '\nIn file: ' 
            + str(fname))
        print('Raw message from device: ' + line)
        sys.exit(10)
    return status



# Test Program
def test(port):

#    init_comm("Com4")
    init_comm(port)


    volts_setpoint_set(5.5)
    amps_setpoint_set(0.50)
    output_state(1)

    time.sleep(1)

    print ("Setpoints")
    print (volts_setpoint_get())
    print (amps_setpoint_get())

    print ()

    for i in range(5):
        volts_setpoint_set((i+1) * 1)
        time.sleep(0.5)
        print (volts_meas())
        print (amps_meas())

    print()
    print (status_get())

    output_state(0)

    print (status_get())

    end_comm()

    print("Done\n")



#test(port)
