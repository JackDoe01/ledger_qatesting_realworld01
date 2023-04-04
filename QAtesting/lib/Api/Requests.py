from SysMan import * ### import all basic functions from a custom library

### Module Overview ##############################################################################
##################################################################################################
### This module takes care of managing the send-response of requests, plus formatting raw data
##################################################################################################

class GenerateUrl():
    ### generate the right url for different cases (different routes endpoints, by now we probably use only "/api/users")
    def __init__(self):
        self.users = config.api_base_url+"users"
        self.login = self.users+"/login"
            
class AddUser(GenerateUrl):
    def __init__(self, user_data):
        super().__init__()
        self.url = self.users
        self.user_data = user_data
        self.headers = {"Content-Type": "application/json"
                        }
        self.req_data = {"user": {"username": self.user_data["name"], 
                                  "email": self.user_data["email"], 
                                  "password": self.user_data["password"]
                                }
                        }
        SysLogInfo("Sending API request: generate new user...")
        self.response = requests.post(self.url, headers=self.headers, json=self.req_data)
        SysLogInfo("API request sent")
        self.response_report = ResponseReport(self.response)
        
class AuthUser(GenerateUrl):
    def __init__(self, user_data):
        super().__init__()
        self.url = self.login
        self.user_data = user_data
        self.headers = {"Content-Type": "application/json",
                        }
        self.req_data = {"user": {
                                  "email": self.user_data["email"], 
                                  "password": self.user_data["password"]
                                }
                        }
        SysLogInfo("Sending API request: auth user...")
        self.response = requests.post(self.url, headers=self.headers, json=self.req_data)
        SysLogInfo("API request sent")
        self.content, self.headers = ResponseReport(self.response)

def DecodeResponseBoby(res_body):
    ### make the response body (content) usable and decoded.
    return json.loads(res_body.decode("utf-8")) ### the response.content object must be decoded-->string-->dict. jsonload output a dict from a string

def ResponseReport(response):
    ###Analyze a response and generate a formatted report
    response_content =  {
                        "url":response.url, 
                        "request":str(response.request.method),
                        "status_code":str(response.status_code), 
                        "reason":str(response.reason), 
                        "content_type":str(response.headers["content-type"]),
                        "elapsed_seconds":json.loads(str(response.elapsed.total_seconds())), 
                        "encoding":str(response.encoding), 
                        "content":DecodeResponseBoby(response.content)
                        }
    
    response_headers={}
    for head in response.headers:
        response_headers[head]=response.headers[head]
    return response_content, response_headers
