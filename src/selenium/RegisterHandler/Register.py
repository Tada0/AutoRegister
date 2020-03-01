from src.xlsx.XLSXHandler import XLSXHandler
from selenium.webdriver import Chrome
from typing import List
import time


class Register:
    @staticmethod
    def execute(driver: Chrome, user: List[str]) -> str:
        Register.fill_inputs(driver, user)
        Register.click_register_button(driver)
        return Register.fetch_registration_result(driver)

    @staticmethod
    def fill_inputs(driver: Chrome, user: List[str]):
        for field in XLSXHandler.REQUIRED_COLUMNS:
            driver.find_element_by_xpath(f'//input[@id="{field.replace(" ", "_")}"]').send_keys(user[field])
            time.sleep(2)

    @staticmethod
    def click_register_button(driver: Chrome):
        driver.find_element_by_xpath('//input[@id="submit"]').click()
        time.sleep(2)

    @staticmethod
    def fetch_registration_result(driver: Chrome) -> str:
        xpath = '//div[@class="large_text"]'
        return ' '.join([element.get_attribute('innerText') for element in driver.find_elements_by_xpath(xpath)])
