import os
import sys
import io
import datetime

### Module Overview ##############################################################################
##################################################################################################
### This is the configuration file where we set all the system default variables that we need
### We also check the system for useful informations like the username, hostname, etc.
##################################################################################################
####################################### DEFAULT VARIABLES DEFNITION ##############################

def GetCurrentTime():                   
    ### we will use the tests pipeline start time as name for logs files
    today_date=datetime.date.today()

    current_time = datetime.datetime.now()
    str_current_time = current_time.strftime("%Y%m%d%H%M%S")
    
    return str_current_time

program_folder = os.path.dirname(os.path.realpath(__file__))+"/"    ### get the folder where the program is running
start_time = GetCurrentTime()               ### we will use the tests pipeline start time as name for logs files
### get some useful system info to generate filepaths etc
os_user_name = os.environ.get('USER')
os_host_name = os.uname()[1]
system_architecture=os.uname()[4]
home_folder=os.path.expanduser("~")+"/"
##########################################################

sys_config_folder=home_folder+".config/"    ### the location of this acrual config file
program_lib_folder=program_folder+"lib/"    ### all stack modules are here
program_logs_folder=program_folder+"logs/"  ### we will save tests logs and system logs here
tests_folder=program_lib_folder+"Tests/"    ### all tests modules are here
reports_folder=program_folder+"reports/"    ### where the tests reports are saved

#################### logger configs:
logs_filepath=program_logs_folder+"logs_"+start_time+".log"    # save the logs path
############# define the empty log handler that will be initialized at first during runtime init (module: SysMan.InitSysLogger())
syslog=None
############# tell the log manager to also print or not the logs at screen
sys_quite_log=False      #if sys_quite_log == True the system logger will not print anything on screen, else it will (leave it True, if not: messy!)

############### browsers configs
### We define here all default settings and paths for the Chrome browser
chrome_config={
        "bin_location":"/bin/google-chrome", ### the actual exe of google-chrome, NOT the webdriver
        "exe_path":"/bin/chromedriver", ### the chrome webdriver
        }
### Web Env config
landing_page="http://localhost:3000/"
api_base_url="http://localhost:3000/api/"

################################# Wait management
page_load_wait=10     ### setup a maximum amount of seconds to wait before page loading
element_load_wait=5   ### setup a maximum amount of seconds to wait before element search fail

################################ Users management
test_user01={
    "name":"testuser01",
    "email":"testuser01@testmail.com",
    "password":"pass123",
    "token":""
    }
############################### Articles management
default_articles_tex={  #Articles creation default injection data
    "title":"test title ",
    "description":"test description ",
    "main_text":"this is the test article main text ",
    "tags":"tags "
    }
created_articles_ids=[] #a list where we will store the id of the articles we will create
