# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 18:32:29 2018

Lib for DAQ

@author: Mike
"""

import TP3005P as tpl
import support_lib as lib
# ^ earlier this was imported as lib, but now a support lib needs this designation
from datetime import datetime
#import numpy as np

import matplotlib.pyplot as plt

# burner dev code that would come from thecaller to this lib
conf = lib.getConf()
tpl.init_comm(conf['serial port'])
##

# This code was developed to benchmark a Harbor Freight drill, whose motors
# are harvested for robot drive systems. V/A examples are for that or PSU maxs.

tpl.volts_setpoint_set(18)
tpl.amps_setpoint_set(5.2) # this is the max that the TP3005P will go to using the hardware UI
tpl.output_state(1)

# Begin recording data

data_dict = {}
# try predef for speed?
data_dict['voltage'] = []
#data_dict['current'] = {'amp_list':[]}
data_dict['current'] = []

# run loop for preset amoutn of time https://stackoverflow.com/questions/24374620/python-loop-to-run-for-certain-amount-of-seconds
import time
#t_end = time.time() + 60 * 15 # this is 15 min * 60 sec as per linked thread
t_end = time.time() + 10 # this should be 10 sec
#while True:
while time.time() < t_end:
#    date = datetime.now()
#    data_dict['voltage'].append([date, tpl.volts_meas()])   # Not sure if this would lead to inaccuracy or not
    data_dict['voltage'].append([datetime.now(), tpl.volts_meas()])   
    data_dict['current'].append([datetime.now(), tpl.amps_meas()])

tpl.output_state(0)
tpl.end_comm()
#tpl.volts_setpoint_get()
#tpl.volts_meas()
#tpl.status_get()


# PLOT!!!!!!!!!!!!
plt.figure()
plt.plot(data_dict['voltage'][:][0], data_dict['voltage'][:][1])
plt.xlabel('datetime')
plt.show()

''' loading/saving
pickle.dump(data_dict, open('data_dict_04142018.p','wb'))

#load:
data_dict = pickle.lload(open('data_dict_04142018.p',rb'))
'''