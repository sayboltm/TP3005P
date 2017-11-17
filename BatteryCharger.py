# A battery charger library

import TP3005P as lib
import sys
import time

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

def ChargeBattery():
    target_OCV = 8.2 # (V)
    C_min = 0.3
    C_max = 1.0
    batt_cap = 1 # (Ah) -- that's AMP HOURS!!
    C_cutoff = 0.05 # (or C/20)
    sleep_time = 1

    # 1. Establish comms
    # 2. Set voltage to target_SoC, i to min, and turn on.
    lib.volts_setpoint_set(target_OCV)
    lib.amps_setpoint_set(C_min*batt_cap)
    lib.output_state(1)
    charging = True
    # 3. Loop/monitor charging, adjusting rate
    def CrateDetect(OCV):
        # 7.75 ~= 52%
        # 8.08 ~= 78%
        # 8.2 ~= 91%
        C_min = 0.3
        target_OCV = 8.2
        if OCV <= 6:
            # Danger low
            Crate = C_min
        elif (OCV > 6) and (OCV <= 7):
            Crate = 0.4
        elif (OCV > 7) and (OCV <= 7.25):
            Crate = 0.5
        elif (OCV > 7.25) and (OCV <= 7.50):
            Crate = 0.8
        elif (OCV > 7.50) and (OCV <= target_OCV):
            Crate = 1.0
        else:
            # SHTF
            print('[-] TSHTF!! Kill all immediately! Stopping')
            lib.output_state(0)
            sys.exit(1)
        return Crate

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

