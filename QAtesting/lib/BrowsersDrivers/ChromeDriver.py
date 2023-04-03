########################################### IMPORT CUSTOM MODULES:
from SysMan import * ### import all basic functions for system management

########################################## IMPORT SELENIUM LIBRARIES:
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as COptions
from selenium import webdriver


                    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ########################### WEBDRIVER MANAGEMENT ### ################################ ### ### ### 
        ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
                    ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

        
def ChDriver():
    options = COptions()
    options.binary_location= config.chrome_config["bin_location"] ### the location of "google-chrome-stable" file in the system           
    ### disable "this browser being automated" prompt and set the proper env to run in a container:
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("prefs", {"credentials_enable_service": False}) ### disable chrome prompt to save your logins and passwords
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--no-sandbox')
    
    options.headless = True
    #options.add_argument("window-size=1280,768")       ### resize window if needed 
    
    service = ChromeService(executable_path=config.chrome_config["exe_path"])   ### the location of the chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver
    
def KillDriver(driver):
    if driver:
        try:
            driver.quit()
            return True
        except Exception as bdkill:
            return False
    else:
        return False
            
    
                   ### ###### ### ### ### ###### ### ### ### ###### ### ### ###
         ###### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ### ###
### ### ### ### ### ### ### ### ### ###### ### ### ### ###### ### ### ### ###### ### ### ### ######
##########END################# WEBDRIVER MANAGEMENT ### ############END#################### ### ### ###
