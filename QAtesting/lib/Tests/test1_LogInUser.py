from SysMan import * ### import all basic functions from a custom library
### ### ### ### ############################ 
from Actions import Navigate
from Actions import Input

### Sign In as a registered user
class run():
    def __init__(self, driver):
        self.test_number = 1
        self.driver = driver
        self.test_report=Report(self.test_number)    ### Init the test report object
        
        Navigate.SignInPage(self.driver)
        self.test_report.Add({"User data input": config.test_user01})
        
        self.logged_profile_link = Input.LogInUser(self.driver, config.test_user01)
        self.test_report.Add({"User logged in":
                            str(self.logged_profile_link)
                            })
        self.test_report.Dump()
