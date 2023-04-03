#!/usr/bin/env python
import sys
import pytest 
sys.path.append('./QAtesting') ### fix import error in GitHub Workflows environment ###
import config                # import all handmade system variables
########################################### 
sys.path.insert(0, config.program_lib_folder)   # make python searching our custom modules folder
from SysMan import *                            # import all basic functions from a custom library
### ### ### ### ############################ import the Chrome webdriver modules
from BrowsersDrivers import ChromeDriver
### ### ### ### ############################ import all tests modules
from Tests import *

### ### ### ### ### ### ### ### ### ######################################## Setup the environment
CleanSystemInit()
config.syslog = InitSysLogger() ### define "syslog" object to be used as handler to write system logs to file: config.system_log_filepath
### #### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

@pytest.fixture(scope="module")          ### init the Chrome Webdriver in a way that pytest can pass it between tests.
def driver():                            
    return ChromeDriver.ChDriver()                   

def test_0(driver):   
    SysLogInfo("Starting test0_CreateNewUser")
    run_output = test0_CreateNewUser.run(driver=driver) 
    assert run_output.logged_profile_link == config.landing_page+"profile/"+config.test_user01["name"]                                                                                                          
                                                                                
def test_1(driver):   
    SysLogInfo("Starting test1_LogInUser")
    run_output = test1_LogInUser.run(driver=driver) 
    assert run_output.logged_profile_link == config.landing_page+"profile/"+config.test_user01["name"]
    
def test_2(driver):   
    SysLogInfo("Starting test2_WriteNewArticle")
    run_output = test2_WriteNewArticle.run(driver=driver) 
    expected_title = config.default_articles_tex["title"]+run_output.article_id
    expected_text = config.default_articles_tex["main_text"]+run_output.article_id
    assert expected_title == run_output.article_content.article_title       ### check the article title match with article id
    assert expected_text == run_output.article_content.article_main_text    ### check the article text match with article id
    
def test_3(driver):   
    SysLogInfo("Starting test3_AddArticleToFavorites")
    run_output = test3_AddArticleToFavorites.run(driver=driver)
    ChromeDriver.KillDriver(driver)
    assert run_output.success_flag == True       # The flag will be true if the favorite button is changed 
    
def test_4():   
    SysLogInfo("Starting test4_APIauthUser")
    run_output = test4_APIauthUser.run() 
    api_response_content = run_output.response.content
    api_response_headers = run_output.response.headers
    assert api_response_content["status_code"] == "200"   
    assert api_response_content["content"]["user"]["username"] == config.test_user01["name"]   
    assert api_response_content["content"]["user"]["email"] == config.test_user01["email"]
    assert api_response_headers["Content-Type"]  == "application/json; charset=utf-8"
    assert api_response_headers["Access-Control-Allow-Origin"]  == "*"
    assert api_response_headers["Vary"]  == "X-HTTP-Method-Override"
    assert api_response_headers["Access-Control-Allow-Origin"]  == "*" 
    assert api_response_headers["Connection"]  == "keep-alive"
    assert api_response_headers["Keep-Alive"]  == "timeout=5"
