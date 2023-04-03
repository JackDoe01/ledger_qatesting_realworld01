from SysMan import * ### import all basic functions from a custom library
### ### ### ### ############################ 
from BrowsersDrivers import ChromeDriver
from Actions import Navigate
from Actions import Input

### Create a new user with static user data from config.test_user01
class run():
    def __init__(self, driver):
        self.test_number = 0
        self.driver = driver
        self.test_report=Report(self.test_number)    ### Init the test report object
        
        Navigate.LandingPage(self.driver)
        Navigate.SignUpPage(self.driver)

        ### store the web element of the new user profile button, in case of test success
        self.logged_profile_link = Input.CreateNewUser(self.driver, config.test_user01)
        self.test_report.Add({"New user profile link":
                        str(self.logged_profile_link)   
                        })
        Input.LogOut(self.driver, config.test_user01)           ### logout to perform the next test (login)
        self.test_report.Dump()
