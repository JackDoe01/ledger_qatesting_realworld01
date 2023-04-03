from SysMan import * ### import all basic functions from a custom library
### ### ### ### ############################ 
from BrowsersDrivers import ChromeDriver
from Actions import Navigate
from Actions import Waits
from Actions import Locate
from Actions import Input

### Write a new article 
class run():
    def __init__(self, driver):
        self.test_number = 2
        self.driver = driver
        self.test_report=Report(self.test_number)    ### Init the test report object
        
        ### generate a random integer string that differentiate all the default text strings from one test to another (article ID)
        self.article_id =str(random.randint(0, 10000000000)) 
        Navigate.NewArticlePage(self.driver)
        Input.WriteNewArticle(self.driver, self.article_id)

        ### locate article elements for analysis
        self.article_content = Locate.ArticlePageElements(self.driver) 
        self.test_report.Add({"New article elements":
            {"ID": self.article_id,
             "title": self.article_content.article_title,
             "text" : self.article_content.article_main_text
            }
            })
        self.test_report.Dump()
        ### we store the article ID for later use  
        config.created_articles_ids.append(self.article_id)
