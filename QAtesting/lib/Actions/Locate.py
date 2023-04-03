########################################### IMPORT CUSTOM MODULES:
from SysMan import * ### import all basic functions for system management

############################################ IMPORT SELENIUM MODULES
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.relative_locator import locate_with

###########################################
from Actions import Waits   ### import our module that takes care of waiting for page loads, element visibility and so on
from Actions.Waits import *

### Module Overview ##############################################################################
##################################################################################################
### This module takes care of defining all the common functions to locate elements inside the DOM
##################################################################################################

############################################################# Decorator to manage errors while locating elements
def Tester(input_module):
    def wrapper(self, *args, **kwargs):
        try:
            module_output = input_module(self, *args, **kwargs)
            if module_output:
                return module_output
        except Exception as no_elem:
            SysLogError("Locate(): element not found: "+self.parameter)
            return None
    return wrapper
###### ### END ### ######################################################################################### Decorator ### END ###
class Elements():
    ### Locate all elements inside the DOM. It will return a list of elements 
    ### Usage example:
      # Locate.Elements(driver, "div").ByTagName()
    #############################################
    
    def __init__(self, driver, parameter):
        self.driver = driver
        self.parameter = parameter
    
    @Tester
    def ByID(self):
        return self.driver.find_elements(By.ID, self.parameter)
    @Tester
    def ByName(self):
        return self.driver.find_elements(By.NAME, self.parameter)
    @Tester
    def ByXPath(self):
        return self.driver.find_elements(By.XPATH, self.parameter)
    @Tester
    def ByLinkText(self):
        return self.driver.find_elements(By.LINK_TEXT, self.parameter)
    @Tester
    def ByTagName(self):
        return self.driver.find_elements(By.TAG_NAME, self.parameter)
    @Tester
    def ByClassName(self):
        return self.driver.find_elements(By.CLASS_NAME, self.parameter)
    @Tester
    def ByCssSelector(self):
        return self.driver.find_elements(By.CSS_SELECTOR, self.parameter)

class Element():
    ### Locate a specific element inside the DOM. It will return the element object
    ### Usage example:
      # Locate.Element(driver, "div").ByTagName()
    #############################################
    
    def __init__(self, driver, parameter):
        self.driver = driver
        self.parameter = parameter
    
    @Tester
    def ByID(self):
        return self.driver.find_element(By.ID, self.parameter)
    @Tester
    def ByName(self):
        return self.driver.find_element(By.NAME, self.parameter)
    @Tester
    def ByXPath(self):
        return self.driver.find_element(By.XPATH, self.parameter)
    @Tester
    def ByLinkText(self):
        return self.driver.find_element(By.LINK_TEXT, self.parameter)
    @Tester
    def ByTagName(self):
        return self.driver.find_element(By.TAG_NAME, self.parameter)
    @Tester
    def ByClassName(self):
        return self.driver.find_element(By.CLASS_NAME, self.parameter)
    @Tester
    def ByCssSelector(self):
        return self.driver.find_element(By.CSS_SELECTOR, self.parameter)
    
class InnerElements():
    ### Locate all elements inside a DOM element. It will return a list of elements 
    ### Usage example:
      # Locate.InnerElements(my_element, "div").ByTagName()
    #############################################
    
    def __init__(self, element, parameter):
        self.element = element
        self.parameter = parameter
    
    @Tester
    def ByID(self):
        return self.element.find_elements(By.ID, self.parameter)
    @Tester
    def ByName(self):
        return self.element.find_elements(By.NAME, self.parameter)
    @Tester
    def ByXPath(self):
        return self.element.find_elements(By.XPATH, self.parameter)
    @Tester
    def ByLinkText(self):
        return self.element.find_elements(By.LINK_TEXT, self.parameter)
    @Tester
    def ByTagName(self):
        return self.element.find_elements(By.TAG_NAME, self.parameter)
    @Tester
    def ByClassName(self):
        return self.element.find_elements(By.CLASS_NAME, self.parameter)
    @Tester
    def ByCssSelector(self):
        return self.element.find_elements(By.CSS_SELECTOR, self.parameter)
    
class InnerElement():
    ### Locate 1 element inside another DOM element. It will return the located element 
    ### Usage example:
      # Locate.InnerElement(my_element, "div").ByTagName()
    #############################################
    def __init__(self, element, parameter):
        self.element = element
        self.parameter = parameter
    
    @Tester
    def ByID(self):
        return self.element.find_element(By.ID, self.parameter)
    @Tester
    def ByName(self):
        return self.element.find_element(By.NAME, self.parameter)
    @Tester
    def ByXPath(self):
        return self.element.find_element(By.XPATH, self.parameter)
    @Tester
    def ByLinkText(self):
        return self.element.find_element(By.LINK_TEXT, self.parameter)
    @Tester
    def ByTagName(self):
        return self.element.find_element(By.TAG_NAME, self.parameter)
    @Tester
    def ByClassName(self):
        return self.element.find_element(By.CLASS_NAME, self.parameter)
    @Tester
    def ByCssSelector(self):
        return self.element.find_element(By.CSS_SELECTOR, self.parameter)


def YourFeedButton(driver):
    ### Find the button "your feed" into the home page
    yfeed_button = None
    candidate_elements = Elements(driver, "link.nav-link").ByClassName() 
    for elem in candidate_elements:
        if elem.text.strip() == "Your Feed":
            yfeed_button = elem
    return yfeed_button

def GlobalFeedButton(driver):
    ### Find the button "global feed" into the home page
    global_button = None
    candidate_elements = Elements(driver, "link.nav-link").ByClassName() 
    for elem in candidate_elements:
        if elem.text.strip() == "Global Feed":
            global_button = elem
    return global_button
        
class SignOutButton():
    ### Locate the SignOut button element inside a page. 
    def __init__(self, driver):
        self.driver = driver
        self.button = Element(driver, "btn.btn-outline-danger").ByClassName()
            
class UserProfileButton():
    ### Locate the username button at the top right corner of screen 
    def __init__(self, driver, user_data):
        self.driver = driver
        self.user_data = user_data
        self.username = user_data["name"]
        self.button_link = "/profile/"+self.username
        self.button = None
        self.candidate_elements = Elements(driver, "nav-link").ByClassName()
        for elem in self.candidate_elements:
            if self.button_link in elem.get_attribute("href"):
                self.button = elem
                break
            
class SettingsButton():
    ### Locate the username button at the top right corner of screen 
    def __init__(self, driver):
        self.driver = driver
        self.button = None
        self.candidate_elements = Elements(driver, "nav-link").ByClassName()
        for elem in self.candidate_elements:
            if "/settings" in elem.get_attribute("href"):
                self.button = elem
                break
    
class SignUpButton():
    ### Locate the SingIn button element inside a page. 
    def __init__(self, driver):
        self.driver = driver
        self.button = None
        self.candidate_elements = Elements(driver, "nav-link").ByClassName()
        for elem in self.candidate_elements:
            if "/user/register" in elem.get_attribute("href"):
                self.button = elem
                break
            
class SignInButton():
    ### Locate the SingIn button element inside a page. This is the login button to login a registered user 
    def __init__(self, driver):
        self.driver = driver
        self.button = None
        self.candidate_elements = Elements(driver, "nav-link").ByClassName()
        for elem in self.candidate_elements:
            if "/user/login" in elem.get_attribute("href"):
                self.button = elem
                SysLogInfo("Locate.SignInButton(): button element found")
                break
        
class SignUpForm():
    ### locate the sign up form container and init an object for all useful element to perform an input to:
    #   user name box
    #   email box  
    #   password box
    #   sign up button to be clicked
    def __init__(self, driver):
        self.driver = driver
        ###locate the container with all signgup input boxes
        self.form_container_element = Element(self.driver, "col-md-6.offset-md-3.col-xs-12").ByClassName() 
        self.candidate_elements = InnerElements(self.form_container_element, "form-control.form-control-lg").ByClassName()
        ### create an object for every input box in the form:
        for elem in self.candidate_elements:
            if elem.get_attribute("placeholder").strip() == "Username":
                self.name_box = elem 
            elif elem.get_attribute("placeholder").strip() == "Email":
                self.email_box = elem
            elif elem.get_attribute("placeholder").strip() == "Password":
                self.password_box = elem
        #locate the submit button:
        self.sign_up_button = InnerElement(self.form_container_element, "btn.btn-lg.btn-primary.pull-xs-right").ByClassName()

class SignInForm():
    ### locate the sign in form container and init an object for all useful element to perform an input to:
    #   email box  
    #   password box
    #   sign in button to be clicked
    def __init__(self, driver):
        self.driver = driver
        ###locate the container with all signgup input boxes
        self.form_container_element = Element(self.driver, "col-md-6.offset-md-3.col-xs-12").ByClassName() 
        #locate inner elements input boxes:
        self.input_candidates= InnerElements(self.form_container_element, "form-control.form-control-lg").ByClassName()
        for elem in self.input_candidates:
            if elem.get_attribute("type") == "email":
                self.email_box = elem
            elif elem.get_attribute("type") == "password":
                self.password_box = elem
        self.sign_in_button = InnerElement(self.form_container_element, "btn.btn-lg.btn-primary.pull-xs-right").ByClassName()        

class NewArticleButton():
    ### locate the "New Article" button inside the page
    def __init__(self, driver):
        self.driver = driver
        self.button = None
        self.candidate_elements = Elements(driver, "nav-link").ByClassName()
        for elem in self.candidate_elements:
            if config.landing_page+"editor" == elem.get_attribute("href"):
                self.button = elem
                SysLogInfo("Locate.NewArticleButton(): button element found")
                break
            
class NewArticleEditor():
    ### Locate the new article editor container and init all the useful objects
    #   to be used to inject text:
    #   title
    #   description
    #   article main text
    #   tags
    ### The text injected will be taken from a dict with some default test text strings: [config.default_articles_tex]
    def __init__(self, driver):
        SysLogInfo("Locate.NewArticleEditor: locating the editor inside the page...")
        self.driver = driver
        ### locate the article editor container element inside the DOM
        self.editor_container_element = Element(self.driver, "col-md-10.offset-md-1.col-xs-12").ByClassName() 
        ### locate the inner input for the article title
        self.title_box = InnerElement(self.editor_container_element, "form-control.form-control-lg").ByClassName() 
        SysLogInfo(self.title_box.get_attribute("placeholder"))
        self.box_candidates =  InnerElements(self.editor_container_element, "form-control").ByClassName()
        for elem in self.box_candidates:
            if "this article about" in elem.get_attribute("placeholder"):
                self.description_box = elem
            elif "Write your article" in elem.get_attribute("placeholder"):
                self.maintext_box = elem
            elif "Enter tags" in elem.get_attribute("placeholder"):
                self.tags_box = elem
        self.publish_button = InnerElement(self.editor_container_element, "btn.btn-lg.pull-xs-right.btn-primary").ByClassName()  
        
class ArticlePageElements():
    ### Create an object for every interesting element in a newly created article page.
    def __init__(self, driver):
        self.driver = driver
        SysLogInfo("Locate.ArticlePageElements: locating new article elements...")
        
        ### locate article page main container:
        self.article_main_container = Element(self.driver, "article-page").ByClassName()
        if self.article_main_container:
            ### locate the article title container:
            self.article_title_container = InnerElement(self.article_main_container, "banner").ByClassName()
            if self.article_title_container:
                self.article_title_container = InnerElement(self.article_title_container, "container").ByClassName()
                #### Get the article title text
                self.article_title = InnerElement(self.article_title_container, "h1").ByTagName().text
        ### Locate the article content:
        self.article_content = Element(self.driver, "row.article-content").ByClassName()
        self.article_content = InnerElement(self.article_content, "col-md-12").ByClassName()
        self.content_elements = InnerElements(self.article_content, "p").ByTagName()
        self.article_main_text = self.content_elements[0].text

def AllArticlesInGlobalFeed(driver):
    ### locate all articles previews elements into the home pages
    SysLogInfo("Locate.AllArticlesInHomePage(): locating all articles previews elements...")
    ### wait until global field is populated and then return the articles previews list:
    for i in range (0, config.element_load_wait):
        if Elements(driver, "article-preview").ByClassName():
            ### return the complete list of articles "hrefs" found in the home page
            return Elements(driver, "article-preview").ByClassName()
        else:
            time.sleep(0.5)

def FavoriteButtonFromArticlePage(driver):
    return Element(driver, "favorite-bottom").ByID()

def ArticleCommentInputBox(driver):
    ### find all candidate elements before selecting the actual box
    input_box = None
    candidate_elements = Elements(driver, "form-control").ByClassName() 
    for elem in candidate_elements:
        if "Write a comment" in elem.get_attribute("placeholder"):
            input_box = elem
    return input_box    ### return the input box object for test validation
