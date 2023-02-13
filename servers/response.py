from selenium import webdriver

from servers.timer import timer


class response:

    def get(url: str):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(60)  # seconds
        try:
            driver.get(url)
            return driver.page_source
        except:
            return None
