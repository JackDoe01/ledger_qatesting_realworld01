########################################### IMPORT CUSTOM MODULES:
from SysMan import * ### import all basic functions for system management

from BrowsersDrivers.ChromeDriver import ChDriver ### import the Chrome selenium webdriver modules

from Actions import Waits          ### import our module that takes care of waiting for page loads, element visibility and so on
from Actions.Waits import *        
from Actions import Locate         ### import our module that takes care of locating elements into the DOM
from Actions import Input          ### import all modules dedicated to input actions like click etc 

### Module Overview ##############################################################################
##################################################################################################
### This module takes care of navigating among the different pages of the test pipeline
##################################################################################################

#################################### NAVIGATION MODULES #######################################################
class NewPage(): 
    ### generic module to open a new webpage
    def __init__(self, driver, url):
        self.url = url
        self.driver = driver
        if self.driver:
            SysLogInfo("Navigate.NewPage(): driver was found ")
        self.Open(self.url)
        
    def Open(self, url):
        SysLogInfo("Navigate.NewPage(): opening page: "+url)
        self.driver.get(url)

class LandingPage(NewPage):
    def __init__(self, driver):
        super().__init__(driver, config.landing_page)   ### inherit the NewPage module classes for simplicity
        self.driver = driver
        self.page_out = None ###        init the output object to track the page behaviour
        SysLogInfo("Navigate.LandingPage() waiting for page load...")
        try:
            Waits.LandingPage(self.driver)   ### wait for the page to be loaded
        except Exception as bd_load:
            SysLogError("Navigate.LandingPage(): page not loaded:")
            SysLogError(bd_load)

class HomePage(NewPage):
    ### Navigate to the landing page as a registered user, which will be different from the standard landing page.
    def __init__(self, driver):
        super().__init__(driver, config.landing_page)   ### inherit the NewPage module classes for simplicity
        self.driver = driver
        self.page_out = None        ### init the output object to track the page behaviour
        SysLogInfo("Navigate.HomePage() waiting for page load...")
        try:
            Waits.HomePage(self.driver)   ### wait for the page to be loaded
        except Exception as bd_load:
            SysLogError("Navigate.HomePage(): page not loaded:")
            SysLogError(bd_load)

class GlobalFeed(HomePage):
    def __init__(self, driver):
        super().__init__(driver)   ### inherit the HomePage module classes for simplicity
        self.driver = driver
        Input.ClickElement(Locate.GlobalFeedButton(self.driver))

class SignUpPage():
    def __init__(self, driver):
        self.driver = driver
        self.signup_button = Locate.SignUpButton(self.driver).button
        Input.ClickElement(self.signup_button)
        SysLogInfo("Navigate.SignUpPage() waiting for page load...")
        try:
            self.sign_up_form_element = Waits.SignUpPageLoad(self.driver).sign_up_form_element   ### wait for the page to be loaded
        except Exception as bd_load:
            SysLogError("Navigate.SignUpPage(): page not loaded:")
            SysLogError(bd_load)

class SettingsPage():
    def __init__(self, driver):
        self.driver = driver
        self.settings_button = Locate.SettingsButton(self.driver).button
        Input.ClickElement(self.settings_button)
        SysLogInfo("Navigate.SettingsPage() waiting for page load...")
        try:
            Waits.SettingsPage(self.driver)   ### wait for the page to be loaded
            SysLogInfo("Navigate.SettingsPage() page loaded")
        except Exception as bd_load:
            SysLogError("Navigate.SettingsPage(): page not loaded")
            SysLogError(bd_load)

class SignInPage():
    def __init__(self, driver):
        self.driver = driver
        LandingPage(self.driver)    ###Navigate to the landing page where Sign In button is located
        Input.ClickElement(Locate.SignInButton(self.driver).button)
        SysLogInfo("Navigate.SignInPage() waiting for page load...")
        try:
            Waits.SignInPage(driver)      ##Wait for the Sign In page to be properly loaded
        except Exception as bd_load:
            SysLogError("Navigate.SignInPage(): page not loaded:")
            SysLogError(bd_load)

class NewArticlePage():
    def __init__(self, driver):
        self.driver = driver
        new_article_button = Locate.NewArticleButton(self.driver).button
        Input.ClickElement(new_article_button)
        SysLogInfo("Navigate.NewArticlePage() waiting for page load...")
        try:
            Waits.NewArticlePageLoad(self.driver)   ### wait for the page to be loaded
        except Exception as bd_load:
            SysLogError("Navigate.NewArticlePage(): page not loaded:")
            SysLogError(bd_load)
            
class OldArticleLink():
    def __init__(self, driver, selected_article_link):
        self.driver = driver
        self.selected_article_link = selected_article_link
        SysLogInfo("Navigate.OldArticleLink() opening page...")
        try:
            NewPage(self.driver, self.selected_article_link)
            Waits.OldArticlePageLoad(self.driver)   ### wait for the page to be loaded
        except Exception as bd_load:
            SysLogError("Navigate.NewArticlePage(): page not loaded:")
            SysLogError(bd_load)

############# END #################### NAVIGATION MODULES ########################## END #######################
    
    
