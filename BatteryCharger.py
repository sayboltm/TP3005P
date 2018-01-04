# A battery charger library

import TP3005P as lib
import sys
import time

import configparser
import os, sys
# TODO: Move comm init into here


# 1. Establish comm

# 2. Set voltage to goal, current to min. Activate

# 3. Unless at goal SoC, a voltage drop will occur and you will hit the current
# limit just set. Measure the voltage drop, and adjust current limit
# accordingly. I.e., start it off slow if it's at a low SoC

# 4. Keep looping, checking SoC and adjusting current

# 5. Once goal SoC reached, loop monitor current until it reaches C/20

# 6. Shut off power when at target SoC and cutoff current! Kill connection.
#-----------------------------------------------------------------------------
# TODO: Huge inconsistency between Crate and current.. need to fix. but for now
# the numbers work out for a 2S 1000 mAh battery
# TODO: Add custom gentile profile/mode (keep crate low for packs with no
# mfg data sheet)

# TODO: premature cutoff also happens if no pack connected
#    - use timer

'''
This charger function of the PSU is activated by user input 10 on nogui

Need to load charge profiles and ask user which one they want

Then execute using profile found in file
    - option to execute differently, or just make separate charge profile.. i.e. drone 80% SoC

Need less than 0% SoC safe trickle charge with user confirmation that it could blow their house up and they should use safe charging habits.

'''
def getParams():
    ''' Gets charge params and SOC OCV stuff '''
    ''' Asks user what battery they want '''

    config = configparser.ConfigParser()
    config.sections()
    config.read('ChargeProfiles/profiles.ini')
    
    count = 0
    for item in config.sections(): 
        print(item)
        count +=1
    print('Found ' + str(count) + ' configurations.')
    
    # TODO: check for consistent, readable wording
    charge_profile = input('Input which one to explore:\n')
    
    valdict = {}
    soc_ocv_dict = {}
    soc_ocv_conf = configparser.ConfigParser()
    soc_ocv_conf.sections()
    soc_ocv_conf.read('ChargeProfiles/SOC_OCV.ini')
    c_rate_dict = {}
    c_rate_conf = configparser.ConfigParser()
    c_rate_conf.sections()
    c_rate_conf.read('ChargeProfiles/c_rates.ini')
    try:
        for key in config[charge_profile]: 
#            print(key + ': ' + config[somefield][key])
            valdict[key] = float(config[charge_profile][key])
        for key in soc_ocv_conf[charge_profile]:
            soc_ocv_dict[key] = float(soc_ocv_conf[charge_profile][key])
        # TODO: need to make sure soc ocv table is valid!!!!! user might forget to provide one
        for key in c_rate_conf[charge_profile]:
            c_rate_dict[key] = float(c_rate_conf[charge_profile][key])
    #for key in config['LiIon']: print(key)

    #for key in valdict: print(key + ': ' + valdict[key])

    # Need to figure out if should put limits and sococv in one thing.. nested key/vals?? need internet

    except KeyError:
        # TODO: add verbosity
        print('Key error, that was an invalid input, or there is a parameter name mismatch between the params.ini and SOC_OCV.ini.')
    except Exception as e:
        print('[-] SHTF.')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno) # why this not conv to str?
        print('[-] Exception Caught.\nType: ' + str(exc_type) + '\nText: ' 
            + str(e) + '\nLine: ' + str(exc_tb.tb_lineno) + '\nIn file: ' 
            + str(fname))
        sys.exit(10)

    return valdict, soc_ocv_dict, c_rate_dict

def SOCtoOCV(soc, soc_dict, ocv_dict):
#https://stackoverflow.com/questions/7934547/python-find-closest-key-in-a-dictionary-from-the-given-input-key
    ''' gets OCV closest to input SOC '''
    # return value of key closest to input key (soc) (value == the ocv)
    ocv = soc_dict.get(num, soc_dict[min(soc_dict.keys(), key=lambda k: abs(float(k)-soc))])
    return ocv

def OCVtoSOC(ocv, soc_ocv_dict):
    pass
    return soc
def CrateDetect(OCV, c_rate_dict):
    # 7.75 ~= 52%
    # 8.08 ~= 78%
    # 8.2 ~= 91%
#    C_min = 0.3
#    target_OCV = 4.1# TODO: update from above input????
##        target_OCV = 8.2 # TODO: update from above input????
#    if OCV <= 3: # These per cell fracs can probs be found online 
##        if OCV <= 6: # TODO: This is a fraction of 8.2, make it of capacity
##            (Ah)
#        # Danger low, disable output until user says yes.
#        Crate = C_min
#    elif (OCV > 3) and (OCV <= 3.5):
##        elif (OCV > 6) and (OCV <= 7):
#        Crate = 0.4
#    elif (OCV > 3.5) and (OCV <= 7.25/2):
#        Crate = 0.5
#    elif (OCV > 7.25/2) and (OCV <= 7.50/2):
#        Crate = 0.8
#    elif (OCV > 7.50/2) and (OCV <= target_OCV):
#        Crate = 1.0
#    else:
#        # SHTF
#        print('[-] TSHTF!! Kill all immediately! Stopping')
#        lib.output_state(0)
#        sys.exit(1)

    # TODO: add soc/ocv conversion/funcs here or separately
    data.get(num, data[min(data.keys(), key=lambda k: abs(k-num))])

    c_rate_dict.get(num, c_rate_dict[min(c_rate_dict.keys(), key=lambda k: abs(float(k)-num))])
    
    result = sorted(c_rate_dict.items() , key=lambda t : t[1])
    # TODO: clean this up
    for k,v in result:
        print(k,v)
        if k >= current_soc:
            Crate = v
            break
     
    

    return Crate

        
def ChargeBattery():
    # TODO: integrate new getParams() dicts into this
        # This requires either A) (better) sorting, charging based on relative data
        #                      B) based on explicit SOC OCV (say 10% increments or so)
            # Will probably use B since on airplane and no wifi -- easier

    # Get params
    misc_params_dict, soc_ocv_dict, c_rate_dict = getParams()

#    target_OCV = 4.1# (V)
#    target_OCV = 8.2 # (V)
    target_OCV = soc_ocv_dict['100']
#    C_min = 0.3
    C_min = misc_params_dict['Cmin']
#    C_max = 1.0 # TODO: this needs to by dynamically updated, especially the min
    C_max = misc_params_dict['Cmax']
#    batt_cap = 0.650 # (Ah)
#    batt_cap = 1 # (Ah) -- that's AMP HOURS!!
    batt_cap = misc_params_dict['Capacity']

#    C_cutoff = 0.05 # (or C/20)
    C_cutoff = misc_params_dict['Ccutoff']
    sleep_time = 1

    # 1. Establish comms
    # 2. Set voltage to target_SoC, i to min, and turn on.
    lib.volts_setpoint_set(target_OCV)
    lib.amps_setpoint_set(C_min*batt_cap)
    lib.output_state(1)
    charging = True
    # 3. Loop/monitor charging, adjusting rate
    while charging == True:
        # get OCV
        OCV = lib.volts_meas()

        if OCV < target_OCV:
            amps_tmp = lib.amps_meas()
            Crate_tmp = amps_tmp / batt_cap
            Crate = CrateDetect(OCV)
            amps = Crate * batt_cap
            if Crate != Crate_tmp:
                print('Changing Crate. Old:' + str(Crate_tmp) + 
                '\nOldCurrent =' + str(amps_tmp))
                print('Setting Crate to: ' + str(Crate) + '.\nCurrent = ' +
                        str(amps))
                lib.amps_setpoint_set(amps)
                print('Amps now at: ' + str(lib.amps_meas()))

        else:
            # Target ocv reached, now watch the current
            print('Target OCV reached, current decreasing!') 
            while charging == True:
                amps = lib.amps_meas()
                Crate = amps/ batt_cap

                if Crate <= C_cutoff:
                    # C/20 reached TODO: can be accidentally triggered by bad
                    # wimpy connection
                    print('[+] Target SoC reached!\n Amps=' + str(amps) +
                            '\nVolts=' + str(OCV))
                    print('Shutting down machine.')
                    lib.output_state(0)
                    print('Breaking serial connection...')
                    lib.end_comm()
                    charging = False
    #                break
                time.sleep(sleep_time)
        time.sleep(sleep_time)

