from atx.ext.chromedriver import ChromeDriver
from TestBase import UiHelper


class WebviewDriver(UiHelper):
    def __init__(self):
        pass

    def __enter__(self):
        self.driver = ChromeDriver(self.d).driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

