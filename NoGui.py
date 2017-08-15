# nogui library
# Eventually this program will have a GUI for ease of use of non programmers, but QT is a pain, and a backup nogui CLI design with a while loop needs to be used. Also easier to debug quickly.

import sys

def startupNoGUI():
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
            break
        elif mode == 1:
            print('TestPSU (not rly)')
        elif mode == 2:
            print('Test charging function launch (not rly)')
        else
            print('Invalid input! Redo.')
