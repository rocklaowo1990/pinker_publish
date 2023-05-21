from selenium import webdriver

class response:

    def get(url: str):
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)  # seconds
        try:
            driver.get(url)
            return driver
        except:
            return None
