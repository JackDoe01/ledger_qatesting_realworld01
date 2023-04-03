from SysMan import * ### import all basic functions from a custom library
### ### ### ### ############################ 
from Api import Requests

### Perform a request to authenticate a user with mail+password.
### 
class run():
    def __init__(self):
        self.test_number = 4
        self.test_report=Report(self.test_number) 

        self.response = Requests.AuthUser(config.test_user01)   ### the report will contain all params of the request answer
        self.test_report.Add({"API request response content":self.response.content})
        self.test_report.Add({"API request response headers":self.response.headers})
        self.test_report.Dump()
        
