''' Support lib for TP3005P '''
import yaml
import os

def getConf():
    ''' Gets/creates conf file. 
    # TODO: The abstracted function for user input is nice, need one for checking
    # and then loop the whole thing over a list of params
    '''
    
    # File/folder parameters
    conf_folder = 'conf'
    conf_file = conf_folder + '/sysconfig.yml'
    # file_to_operate_on = 'Excel file' # stored in the config yaml
    
    def getUsrInput(field, hint='', extension=None):
        ''' Gets field from user, optionally checks file extn.
            Also, can contain a hint that will be visible to user.
            Example:
                field: 'Excel file'
                hint: 'testBook.xlsx'
                extension: = ('.xls', '.xlsx') 
        '''
        if hint != '':
            # If hint entered, format it as follows:
            hint = '(e.g. ' + hint + ')'

        while True:
            value = input('Input name of ' + field + ': ' + hint + '\n')
            if extension == None:
                break
            else:
                # Check file extn until valid
                if value.lower().endswith(extension):
                    break
                else:
                    print('\nInvalid ' + field + '! Did you forget the file extension?')
        return value 

    def confirmUsrInput(conf, field, value, hint='', extension=None):
        ''' Confirms value of some field, value in a conf dict. '''

        while True:
            usr_input = input(field + ' is: ' + value 
                + '. Is this correct? (y/n)\n')
            if usr_input.lower() == 'y':
                break # Stop if all good
            elif usr_input.lower() == 'n':
                # Else, get input again
                value = getUsrInput(field, hint, extension)
                # And save changes to conf in conf
                conf = flushToConf(conf, field, value, conf_file)
            else:
                print('Invalid input!')
         
    def flushToConf(a_dict, key, value, conf_file):
        ''' Updates key/value in a_dict, and flushes to conf_file '''
        a_dict[key] = value
        with open(conf_file, 'w') as outfile:
            yaml.dump(a_dict, outfile, default_flow_style=False) 
        return a_dict
        
    # Try to open the conf file and get file name
    try:
        with open(conf_file, 'r') as infile:
            conf = yaml.load(infile)
            sys_OS = conf['OS']
            port = conf['serial port']

    except FileNotFoundError:
        # Make folder if DNE
        if not os.path.exists(conf_folder): # TIP: good place for first time setup
            os.makedirs('conf')
        # prompt user for filename
        print('Previous configuration not found.')
        sys_OS = getUsrInput('OS', 'Linux, Windows')
        port = getUsrInput('serial port', '/dev/ttyUSB0 or COM4')
        
        # Save the filename
        conf = {} # create new conf dict, since conf file DNE
        conf = flushToConf(conf, 'OS', sys_OS, conf_file)
        conf = flushToConf(conf, 'serial port', port, conf_file)
        # TODO: de-DRY

    # Make sure user is happy with changes, and/or make sure any previously
    # found name is good.
   
    # Confirm user input. This handles case of conf exist, but value wrong
    confirmUsrInput(conf, 'OS', sys_OS)
    confirmUsrInput(conf, 'serial port', port)
    
    return conf

