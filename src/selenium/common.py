from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


class DriverCommon:
    @staticmethod
    def prepare_chrome_options(headless: bool, working_directory: str) -> Options:
        options = Options()
        options.add_argument("--headless") if headless else None
        options.add_experimental_option("prefs", {
            "download.default_directory": working_directory
        })
        return options

    @staticmethod
    def create_driver(driver_path: str, driver_options: Options) -> Chrome:
        driver = Chrome(executable_path=driver_path, options=driver_options)
        driver.set_window_position(-1920, 0)
        driver.set_window_size(1920, 1080)
        return driver
