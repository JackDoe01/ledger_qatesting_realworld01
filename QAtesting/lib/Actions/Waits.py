########################################### IMPORT CUSTOM MODULES:
from SysMan import * ### import all basic functions for system management

############################################ IMPORT SELENIUM LIBRARIES
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import locate_with

from Actions import Locate

### Module Overview ##############################################################################
##################################################################################################
### This module takes care of defining all different ways we can wait for pageload, elements, etc.
##################################################################################################

############################################################# Decorator: to manage the selenium wait output of all the different use cases
def Tester(input_module):
    def wrapper(self, *args, **kwargs):
        try:
            input_module(self, *args, **kwargs)
            return True
        except Exception as no_elem:
            SysLogError("Waits() timeout expired while waiting for element: "+self.parameter)
            return False
    return wrapper
###### ### END ### ######################################################################################### Decorator ### END ###

class Visible():
    ### Wait n seconds (wait_time) for an element in the DOM to be visible.
    ### Define the element by the paramenter you are looking for
    ### Usage example:
      # Waits.Visible(driver, myseconds, "body").ByTagName()
    #############################################    
    def __init__(self, driver, wait_time, parameter):
        self.driver = driver
        self.wait_time = wait_time
        self.parameter = parameter
    @Tester
    def ByClassName(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, self.parameter)))
    @Tester
    def ByCssSelector(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.parameter)))
    @Tester
    def ByTagName(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.TAG_NAME, self.parameter)))
    @Tester
    def ById(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.ID, self.parameter)))
    @Tester
    def ByXPath(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.visibility_of_element_located((By.XPATH, self.parameter)))

class Present():
    ### Wait n seconds (wait_time) for an element in the DOM to be present (different from visible, can be in background).
    ### Define the element by the paramenter you are looking for
    ### Usage example:
      # Waits.Present(driver, myseconds, "body").ByTagName()
    def __init__(self, driver, wait_time, parameter):
        self.driver = driver
        self.wait_time = wait_time
        self.parameter = parameter
    @Tester
    def ByClassName(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, self.parameter)))
    @Tester
    def ByCssSelector(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.parameter)))
    @Tester
    def ByTagName(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.TAG_NAME, self.parameter)))
    @Tester
    def ById(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.ID, self.parameter)))
    @Tester
    def ByXPath(self):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, self.parameter)))
        
class PageLoad():
    ### Wait n seconds (wait_time) for a page to be generally loaded bt waiting for the body visibility.
    ### Define the element by the paramenter you are looking for
    ### Usage example:
      # Waits.PageLoad(driver, myseconds)
    def __init__(self, driver):
        self.driver = driver
        self.loaded = Visible(self.driver, config.page_load_wait, "body").ByTagName() ###Wait for visibility of page "body"
                                                                               #this usually means that we can start interacting with the DOM
        if not self.loaded:
            SysLogError("Waits.PageLoad(): load fail")
            raise Exception("page load fail: body not found")
        
        
class LandingPage():
    ### Wait for the loading of the home page as NON registered user
    def __init__(self, driver):
        self.driver = driver
        PageLoad(self.driver)   ###wait for body load
        self.loaded = Visible(self.driver, config.page_load_wait, "/html/body/div[1]/div/div[1]/div/h1").ByXPath()
        if self.loaded:
            SysLogInfo("Waits.LandingPage(): load success")
        else:
            SysLogError("Waits.LandingPage(): load fail")
            raise Exception("page load fail: main logo not visible")
        
class HomePage():
    ### Wait for the loading of the home page as registered user
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        ### wait for the article comment input box to be visible, proof the old article page is loaded:
        SysLogInfo("Waits.HomePage(): waiting for page to load...")
        for i in range (0, config.page_load_wait):
            PageLoad(self.driver)   ###wait for body load
            if Locate.YourFeedButton(driver):
                self.loaded = True
                break
            else:
                time.sleep(1)
        if self.loaded:
            SysLogInfo("Waits.HomePage(): page is loaded")
        else:
            raise Exception("page load fail, cannot locate 'your feed' button")
        
class SignUpPageLoad():
    ### wait for page to display "Sign Up" button, proof that a user is logged out
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        ### Wait for the "Sign Up" button until is found, till maximum wait time.
        for i in range (0, config.page_load_wait):
            PageLoad(self.driver)   ###wait for body load
            try:
                self.sign_up_form_element = Locate.SignUpForm(driver).form_container_element
                SysLogInfo("Waits.SignUpPageLoad(): page loaded")
                self.loaded = True
                break
            except Exception as not_load:
                time.sleep(1)
        if not self.loaded:
            SysLogInfo("Waits.SignUpPageLoad(): cannot locate sign up form")
            raise Exception("sign up page load fail: cannot locate sign up form")

class SignUpButton():
    ### wait for page to display "Sign Up" button, proof that a user is logged out
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        ### Wait for the "Sign Up" button until is found, till maximum wait time.
        for i in range (0, config.page_load_wait):
            PageLoad(self.driver)   ###wait for body load
            if Locate.SignUpButton(driver).button:
                SysLogInfo("Waits.SignUpButton(): SignUp button found")
                self.loaded = True
                break
            else:
                time.sleep(1)
        if not self.loaded:
            SysLogInfo("Waits.SignUpButton(): cannot locate user sign up button")
            raise Exception("user login fail: cannot locate user sign up button")
        
class SettingsPage():
    ### wait for page to display "text-xs-center" elements with "Your Settings" text
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        for i in range (0, config.page_load_wait):    
            PageLoad(self.driver)   ###wait for body load
            try:
                if Locate.Element(driver, "text-xs-center").ByClassName().text.strip() == "Your Settings":
                    self.loaded = True
                    break
                else:
                    time.sleep(1)
            except Exception as bd_find:
                time.sleep(1)
        if not self.loaded:
            SysLogInfo("Waits.SettingsPage(): page not loaded")
            raise Exception("SettingsPage load fail: cannot locate center text")
            
class SignInPage():
    ### wait for page to display "Sign Up" button, proof that a user is logged out
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        ### Wait for the "Sign in" container to be visible
        self.loaded = Visible(self.driver, config.page_load_wait, "col-md-6.offset-md-3.col-xs-12").ByClassName()
        if self.loaded:
            SysLogInfo("Waits.SignInPage(): page is loaded")
        else:
            SysLogError("Waits.SignInPage(): load fail")
            raise Exception("page load fail: sign in container not visible")

class UserLoggedIn():
    ### wait for page to display the username at the top right corner of screen
    def __init__(self, driver, user_data):
        self.driver = driver
        self.loaded = None
        ### Wait for the "Sign Up" button until is found, till maximum wait time.
        for i in range (0, config.page_load_wait):
            PageLoad(self.driver)   ###wait for body load
            if Locate.UserProfileButton(driver, user_data).button:
                self.logged_profile_link = Locate.UserProfileButton(driver, user_data).button.get_attribute("href")
                SysLogInfo("Waits.UserLoggedIn(): User profile button found")
                self.loaded = True
                break
            else:
                time.sleep(1)
        if self.loaded:
            SysLogInfo("Waits.UserLoggedIn(): login success")
        else:
            SysLogError("Waits.UserLoggedIn(): cannot locate user profile button  button")
            raise Exception("user login fail: cannot locate user profile button")

class NewArticlePageLoad():
    ### wait for visibility of the new article text editor container by its class name
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        ### Wait for the "Sign in" container to be visible
        self.loaded = Visible(self.driver, config.page_load_wait, "col-md-10.offset-md-1.col-xs-12").ByClassName()
        if self.loaded:
            SysLogInfo("Waits.NewArticlePage(): page is loaded")
        else:
            SysLogError("Waits.NewArticlePage(): load fail")
            raise Exception("page load fail: new article text editor container not visible")        
        
class OldArticlePageLoad():
    ### Wait for the loading of an old article page link
    def __init__(self, driver):
        self.driver = driver
        self.loaded = None
        ### wait for the article comment input box to be visible, proof the old article page is loaded:
        SysLogInfo("Waits.OldArticlePageLoad(): waiting for article page to load...")
        for i in range (0, config.page_load_wait):
            PageLoad(self.driver)   ###wait for body load
            if Locate.ArticleCommentInputBox(driver):   ### if the comment box is present means the page is loaded
                self.report = Locate.ArticleCommentInputBox(driver)
                self.loaded = True
                break
            else:
                time.sleep(1)
        if self.loaded:
            SysLogInfo("Waits.OldArticlePageLoad(): article page is loaded")
        else:
            raise Exception("page load fail, cannot locate comment input box")
