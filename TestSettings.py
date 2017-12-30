''' Test configuration profiles etc. '''

#import yaml
import configparser
import os, sys

config = configparser.ConfigParser()
config.sections()
config.read('ChargeProfiles/profiles.ini')
print(config.sections())

count = 0
for item in config.sections(): 
    print(item)
    count +=1
print('Found ' + str(count) + ' configurations.')

somefield = input('Input which one to explore:\n')

valdict = {}

try:
    for key in config[somefield]: 
        print(key + ': ' + config[somefield][key])
        valdict[key] = config[somefield][key]
#for key in config['LiIon']: print(key)

#for key in valdict: print(key + ': ' + valdict[key])

# Need to figure out if should put limits and sococv in one thing.. nested key/vals?? need internet

except KeyError:
    print('Key error, that was an invalid input')
except Exception as e:
    print('[-] SHTF.')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #print(exc_type, fname, exc_tb.tb_lineno) # why this not conv to str?
    print('[-] Exception Caught.\nType: ' + str(exc_type) + '\nText: ' 
        + str(e) + '\nLine: ' + str(exc_tb.tb_lineno) + '\nIn file: ' 
        + str(fname))
    sys.exit(10)

