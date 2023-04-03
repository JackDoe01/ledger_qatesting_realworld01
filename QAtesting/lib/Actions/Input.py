########################################### IMPORT CUSTOM MODULES:
from SysMan import * ### import all basic functions for system management

from selenium.webdriver.common.keys import Keys  ### import selenium module to inject keys into forms
from Actions import Waits        ### import our module that takes care of waiting for page loads, element visibility and so on
from Actions.Waits import *      ### from waits we will inherit also all the useful selenium modules
from Actions import Locate       ### import our module that takes care of locating elements into the DOM
from Actions import Navigate     ### import our module that takes care of navigating pages

### Module Overview ###########################################################################
###############################################################################################
### This module takes care of defining all the input actions that we will perform on webpages.
###############################################################################################
class InjectText():
    ### Inject keystrokes into forms
    def __init__(self, element, text):
        SysLogInfo("Input.InjectText() injecting text into element: "+text)
        self.element = element      ### the web element where to inject the text
        self.text = text
        self.element.send_keys(self.text)        
    
def ClickElement(element):
    SysLogInfo("Input.ClickElement(): sending click "+str(element))
    try:
        element.click()
        SysLogInfo("Input.ClickElement(): click success")
    except Exception as bd_click:
        SysLogError("Input.ClickElement(): click fail: "+str(element))
        
def CreateNewUser(driver, user_data):
    ### locate the sign up input form inside the sign up page, then fill the forms with a new user login data dict
    ### then check the reloaded page for proof that a new user is created
    SysLogInfo("Input.CreateNewUser(): creating user now...")
    try:
        signup_conatiner = Locate.SignUpForm(driver)
        InjectText(signup_conatiner.name_box, user_data["name"])
        InjectText(signup_conatiner.email_box, user_data["email"])
        InjectText(signup_conatiner.password_box, user_data["password"])
        time.sleep(0.5) ### a little blind sleep is best practice for stability in this case
        ClickElement(signup_conatiner.sign_up_button)
        return Waits.UserLoggedIn(driver, user_data).logged_profile_link #return the logged in user link for test validation
    except Exception as bd_user_input:
        SysLogError("Input.CreateNewUser(): new user creation fail:"+str(bd_user_input))
        
def LogInUser(driver, user_data):
    ### locate the sign in input form inside the sign in page, then fill the forms with a new user login data dict
    ### then check the reloaded page for proof that a new user is logged in
    SysLogInfo("Input.LogInUser(): loggin in user now...")
    try:
        signin_conatiner = Locate.SignInForm(driver)
        InjectText(signin_conatiner.email_box, user_data["email"])
        InjectText(signin_conatiner.password_box, user_data["password"])
        time.sleep(0.5) ### a little blind sleep is best practice for stability in this case
        ClickElement(signin_conatiner.sign_in_button)
        return Waits.UserLoggedIn(driver, user_data).logged_profile_link #return the web element for test success confirm
    except Exception as bd_user_input:
        SysLogError("Input.LogInUser(): user login fail")
        SysLogError(bd_user_input)

def LogOut(driver, user_data):
    ### click "Sign Out" button to log out from user session
    SysLogInfo("Input.LogOut(): loggin out user...")
    try:
        Waits.UserLoggedIn(driver, user_data)     ### be sure that user is logged in
        Navigate.SettingsPage(driver)
        button = Locate.SignOutButton(driver).button
        button.click()
        Waits.SignUpButton(driver)        ### Wait for "Sign Up" button to be reloaded, proof we are logged out
        SysLogInfo("Input.LogOut(): log out success")
    except Exception as bd_logout:
        SysLogError("Input.LogOut(): logout fail:")
        SysLogError(bd_logout)

def WriteNewArticle(driver, custom_integer):
    ### Inject test strings inside all fields of the new article editor and submit the new article by pushing the "Pubish Article" button.
    #   The text is taken from a default test strings dict: config.default_articles_tex upon which we will add a random generated integer
    #   to differenciate by different tests.
    
    SysLogInfo("Input.WriteNewArticle(): writing article now...")
    try:
        article_conatiner = Locate.NewArticleEditor(driver)
        InjectText(article_conatiner.title_box, config.default_articles_tex["title"]+custom_integer)
        InjectText(article_conatiner.description_box, config.default_articles_tex["description"]+custom_integer)
        InjectText(article_conatiner.maintext_box, config.default_articles_tex["main_text"]+custom_integer)
        InjectText(article_conatiner.tags_box, config.default_articles_tex["tags"]+custom_integer)
        time.sleep(0.5) ### a little blind sleep is best practice for stability in this case
        ClickElement(article_conatiner.publish_button)  ###first click just validates the tags field
        time.sleep(0.5) ### a little blind sleep is best practice for stability in this case
        ClickElement(article_conatiner.publish_button)  ###second click actually submit the article after tags field validation
        return Waits.OldArticlePageLoad(driver).report     ###wait for the website to open the saved article page (automatically), return the web element for test validation
    except Exception as bd_artcl:
        SysLogError("Input.WriteNewArticle(): new article creation fail:")
        SysLogError(bd_artcl)
        
def AddLastArticleToFavorites(driver):
    ### Search the last created article ID amongs the articles into the Home Page global feed-->add that to favorites
    add_fav_success= False          #set a flag to register the success/failure of this task
    article_ID= config.created_articles_ids[len(config.created_articles_ids)-1]
    SysLogInfo("Input.AddArticleToFavorites(): adding last article created to favorites")
    SysLogInfo("Input.AddArticleToFavorites(): article ID: "+str(article_ID))
    for elem in Locate.AllArticlesInGlobalFeed(driver):
        ### search amongh all the articles previews link, the ID of the last article we have created
        if article_ID in elem.find_element(By.CLASS_NAME, "preview-link").get_attribute("href"):
            ### We found an ID match, we now procede to add this articles to favorites:
            fav_button_container = elem.find_element(By.CLASS_NAME, "pull-xs-right")
            ### locate the button element identifier before being pushed and save it's state for comparison
            fav_button_pre_element = fav_button_container.find_element(By.CLASS_NAME, "btn.btn-sm.btn-outline-primary")
            button_pre_state = fav_button_pre_element.text  ###store the button state
            ###Click the button
            ClickElement(fav_button_pre_element)
            ###wait to locate the button element identifier after being pushed and save it's state for comparison
            
            for i in range(0, config.element_load_wait):
                try:
                    fav_button_post_element = fav_button_container.find_element(By.CLASS_NAME, "btn.btn-sm.btn-primary")
                    button_post_state = fav_button_post_element.text  ###store the button state
                    if not button_post_state == button_pre_state:
                        add_fav_success= True 
                        SysLogInfo("Input.AddArticleToFavorites(): article added successfully") ### WARNING: MAKE THIS A REPORT
                        break
                    else:
                        time.sleep(0.5)
                except Exception as bd_cycle:
                    time.sleep(0.5)
    return add_fav_success
            
    
    
