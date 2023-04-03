import os
import sys
import traceback
import shutil
import datetime
import random
import time
import json
import requests
import logging     ### standard module for log management

import config   ### import all handmade system variables, this are all the variables needed to run the script and the default settings
                  # this is done via the ./config file, which you can edit to change defaults
                  # for example you can change:
                  #     ./config.sys_quite_log = True
######################################################################################################################################
############################## TIME MANAGEMENT ##############################################
def GetCurrentTime():
    ### we will use this in the logs manager to output messages
    today_date=datetime.date.today()
    current_time = datetime.datetime.now()
    str_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.datetime.strptime(str_current_time, "%Y-%m-%d %H:%M:%S.%f")
    return current_time, str_current_time

######## END ########################### TIME MANAGEMENT ############################### END #############

### ### ### ### ### ### ### ### File management ### ### ### ### ### ### ### ### #########################
def DumpJson(source, file_path):
    ### dump dict and lists in json format
    try:
        with open(file_path, "w") as outfile:
            json.dump(source, outfile, indent=2)
            SysLogDebug("SysMan.DumpJson() file dumped: "+str(file_path))
            return True
    except Exception as bd_dmp:
        SysLogError("SysMan.DumpJson() ERROR whle dumping file: "+str(file_path))
        return None   
############################################################### ### ### ### system cleaner ### ### ### 
class CleanSystemInit():
    def __init__(self):
        self.CleanFolderNoLog(config.program_logs_folder)
        self.CleanFolderNoLog(config.reports_folder)
    ### Clean the system at beginning of runtime.
    ### This comes before we are able to init the syslogger, so we don't log
    def CleanFolderNoLog(self, folderpath):
        if not os.path.exists(folderpath):
            try:
                os.makedirs(folderpath)
            except Exception as bad_folder:
                SysLogError(str(bad_folder))
        else:
            try:
                shutil.rmtree(folderpath, ignore_errors=True)
                os.makedirs(folderpath)
            except Exception as bad_creation:
                SysLogError(str(bad_creation))        
#### END ### ### ### ### ### system cleaner ### ### ###  END ### ### ### 

### END ##### ### ### ### ### ### ### File management ### ### ### ### ### ### ### ### ######## END ########

### ### ### ###################### LOGS MANAGEMENT ############################################ ### ### ###
def InitSysLogger():
    ### Setup the handler to log all system critical events
    sys_logger= logging.getLogger()
    sys_logger.setLevel(logging.DEBUG) ### Setup the default log level
    log_hand = logging.FileHandler(config.logs_filepath, 'w', 'utf-8')  #point the logger to the right syslogger file 
    log_format="[%(asctime)s] [%(name)s:%(levelname)s]: %(message)s" #setup the favourite style of logging
    log_hand.setFormatter(logging.Formatter(log_format)) 
    sys_logger.addHandler(log_hand)
    return sys_logger

################################### print logs on screen:
def SysScreenLogger(message, level):
    ### Setup the handler to print at screen all system critical events
    if not config.sys_quite_log:
        print(GetCurrentTime()[1], "["+level+"]:", message)
        
################################### create precofigured logging handlers to inherit down the stack for simplicity
### Usage example:
  # SysLogDebug("Some interesting thing happened, what a blast!")
  # SysLogWarning("This doesn't feel so right, are u sure we cool!?")
  # To enable, disable the screen printing, edit the variable:
  #     config.sys_quite_log = True (keep it true, if not, it will be messy on screen, read the file afterwards)
  
def SysLogDebug(message):
    SysScreenLogger(message, "SysLog[DEBUG]")
    config.syslog.debug(message)    
def SysLogInfo(message):
    SysScreenLogger(message, "SysLog[INFO]")
    config.syslog.info(message)
def SysLogWarning(message):
    SysScreenLogger(message, "SysLog[WARNING]")
    config.syslog.warning(message)
def SysLogError(message):
    SysScreenLogger(message, "SysLog[ERROR]")
    config.syslog.error(message)
def SysLogCritical(message):
    SysScreenLogger(message, "SysLog[CRITICAL]")
    config.syslog.critical(message)
### END ### ### ###################### LOGS MANAGEMENT ############################################ ### ### END ###

### ### ### ###################### REPORTS MANAGEMENT ############################################ ### ### ###
### Generate reports in json format to store critical tests data 

class Report():
    def __init__(self, test_number):
        self.creation_date = GetCurrentTime()[1]    ###get the time when the report is initiated
        self.test_number = str(test_number)
        self.report_filepath = config.reports_folder+"Report_Test"+self.test_number+"_"+self.creation_date.replace(" ", "_")
        ### fix artifact "spcial characters" error in GitHub Workflows ###
        self.report_filepath = self.report_filepath.replace(":", "").replace(".", "_")
        self.report = []    #Init an object that will be populated with critical test data
        
    def Add(self, entry):
        #add an entry to the report object 
        self.report.append({GetCurrentTime()[1].replace(" ", "_"):entry})
                
    def Dump(self):
        # Dump the report to a json file
        try:
            DumpJson(self.report, self.report_filepath)
            SysLogInfo("Test report dumped to file: "+self.report_filepath)
        except Exception as bd_dmp:
            SysLogError("Report(): file dump failed")
            SysLogError(str(bd_dmp))
### END ### ### ###################### REPORTS MANAGEMENT ############################################ ### ### END ###
