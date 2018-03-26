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
    ''' Gets charge params and SOC OCV stuff. Asks user what battery they want
            Inputs:
                ./ChargeProfiles/SOC_OCV.ini    // SOC OCV table
                ./ChargeProfiles/c_rates.ini    // C-rate at some SOC table
            Returns:
                misc_params_dict: misc. battery params dict
                soc_ocv_dict: SOC: OCV dict
                c_rate_dict: SOC: C-rate lookup dict
    '''
    
    config_folder = 'Config/'

    ### Set up the configparser for all INI files, declare dicts
    # For general/misc battery parameters
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_folder + 'params.ini')
    misc_params_dict = {}
    
    # For SOC/OCV lookup
    soc_ocv_conf = configparser.ConfigParser()
    soc_ocv_conf.sections()
    soc_ocv_conf.read(config_folder + 'SOC_OCV.ini')
    soc_ocv_dict = {}

    # For C-rate/charge profile of some battery
    c_rate_conf = configparser.ConfigParser()
    c_rate_conf.sections()
    c_rate_conf.read(config_folder + 'c_rates.ini')
    c_rate_dict = {}
   
    ### Find configurations, have the user pick a battery
    count = 0
    for item in config.sections(): 
        print(item)
        count +=1
    print('Found ' + str(count) + ' configurations.')
    # TODO: Should check to make valid BEFORE telling the user these are good

    # TODO: check for consistent, readable wording
    charge_profile = input('Input which one to explore:\n')
   
   # TODO: put in while loop in case user enters wrong battery
    # be sure to allow quitting at all times
    # TODO: make a default set of options in some of these?
    try:
        for key in config[charge_profile]: 
#            print(key + ': ' + config[somefield][key])
            misc_params_dict[key] = float(config[charge_profile][key])
        for key in soc_ocv_conf[charge_profile]:
            soc_ocv_dict[float(key)] = float(soc_ocv_conf[charge_profile][key])
        # TODO: need to make sure soc ocv table is valid!!!!! user might forget to provide one or fill with invalid values
        for key in c_rate_conf[charge_profile]:
            c_rate_dict[float(key)] = float(c_rate_conf[charge_profile][key])

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

    return misc_params_dict, soc_ocv_dict, c_rate_dict

def SOCtoOCV(soc, soc_ocv_dict):
    ''' Gets OCV closest to input SOC
            Inputs:
                soc: State of Charge (float/int)
                soc_dict: {SOC: OCV} 
            Outputs:
                ocv: Open circuit voltage (Volts, float)
    '''
#https://stackoverflow.com/questions/7934547/python-find-closest-key-in-a-dictionary-from-the-given-input-key

    # return value of key closest to input key (soc) (value == the ocv)
    ocv = soc_ocv_dict.get(soc, soc_ocv_dict[min(soc_ocv_dict.keys(), key=lambda k: abs(float(k)-soc))])
    return ocv

def OCVtoSOC(ocv, soc_ocv_dict):
    ''' Gets SOC closest to input OCV
            
            Inputs:
                ocv: Open circuit voltage (V, float)
                soc_ocv_dict: {SOC: OCV}
    '''
    # Inverts the dict and runs like SOCtoOCV() 
    inverted_dict = dict([[v,k] for k,v in soc_ocv_dict.items()])
    soc = inverted_dict.get(ocv, inverted_dict[min(inverted_dict.keys(), key=lambda k: abs(float(k)-ocv))])
    return soc 

def CrateDetect(SOC, c_rate_dict):
    ''' Gets closest (rounds down floats to int) Crate from OCV 
        Inputs:
            SOC: State of Charge (float)
            c_rate_dict: {SOC: mfg_recommended_C-rate}
        Outputs:
            nearest_C_rate: closest C-rate based on SOC (float)
    '''
    nearest_C_rate = c_rate_dict.get(SOC, c_rate_dict[min(c_rate_dict.keys(), key=lambda k: abs(float(k)-SOC))])

    return nearest_C_rate
        
def ChargeBattery():
    ''' Main battery charging function. Calls everything necessary to charge connected battery correctly, based on user input and parameter files. See readme for actual file input information.
    '''

    # TODO: Validate with real battery, clean up

    # Get SOC/OCV, allowed C-rates, misc params
    misc_params_dict, soc_ocv_dict, c_rate_dict = getParams()

#    target_OCV = 4.1# (V)
#    target_OCV = 8.2 # (V)
    #TODO: highest in profile, instead of 100. See CrateDetect function for ideas
    target_OCV = soc_ocv_dict[100]
#    C_min = 0.3
    c_min = misc_params_dict['c_min']
#    C_max = 1.0 # TODO: this needs to by dynamically updated, especially the min
    c_max = misc_params_dict['c_max']
#    batt_cap = 0.650 # (Ah)
#    batt_cap = 1 # (Ah) -- that's AMP HOURS!!
    batt_cap = misc_params_dict['capacity']

#    C_cutoff = 0.05 # (or C/20)
    c_cutoff = misc_params_dict['c_cutoff']
    sleep_time = 1

    # 1. Establish comms
    # 2. Set voltage to target_SoC, i to min, and turn on.
    lib.volts_setpoint_set(target_OCV)
    lib.amps_setpoint_set(c_min*batt_cap)
    lib.output_state(1)
    charging = True
    # 3. Loop/monitor charging, adjusting rate
    while charging == True:
        # get OCV
        OCV = lib.volts_meas()
#        SOC = OCVtoSOC(OCV, soc_ocv_dict)
        if OCV < target_OCV: # must be done with measured OCV to avoid rounding/nearest value errors
            amps_tmp = lib.amps_meas()
            Crate_tmp = amps_tmp / batt_cap

            # Wow fail changed so much stuff at once forgot to update this
#            Crate = CrateDetect(OCV)
            Crate = CrateDetect(OCVtoSOC(OCV, soc_ocv_dict), c_rate_dict)
            # TODO: add printout that crate is changing as per the input file
            # TODO: GRAPH the charge profile!? :D lolol
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

                if Crate <= c_cutoff:
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
                time.sleep(sleep_time) # TODO: try lib.delay(secs)
        time.sleep(sleep_time)

