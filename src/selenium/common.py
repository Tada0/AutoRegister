from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import time


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

    @staticmethod
    def open_new_tab(driver: Chrome, url: str) -> None:
        driver.execute_script(f"window.open('')")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)
        time.sleep(2)

    @staticmethod
    def close_current_tab(driver: Chrome) -> None:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
