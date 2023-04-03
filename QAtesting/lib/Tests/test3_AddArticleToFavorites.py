from SysMan import *    ### import all basic functions from a custom library
### ### ### ### ############################ 
from BrowsersDrivers import ChromeDriver
from Actions import Navigate
from Actions import Waits
from Actions import Locate
from Actions import Input

### Add the last created article to favorites from the home page articles list            
class run():
    def __init__(self, driver):
        self.test_number = 3
        self.driver = driver
        self.test_report=Report(self.test_number)    ### Init the test report object
        
        Navigate.GlobalFeed(self.driver)  #navigate to the global feed section of the Home Page
        self.success_flag = Input.AddLastArticleToFavorites(self.driver)  #the flag == True indicate that the favorite button press has being detected
        self.test_report.Add({"Favorite button updated": self.success_flag})
        self.test_report.Dump()
