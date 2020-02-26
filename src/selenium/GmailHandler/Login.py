from typing import Dict
from selenium.webdriver import Chrome
import time


class Login:
    @staticmethod
    def execute(driver: Chrome, credentials: Dict[str, str]):
        """
        Google blocks chrome driver from logging into gmail account, when you attempt it following text is shown:

        **Couldn't sign you in**
        This browser or app may not be secure.
        Try using a different browser.
        If you’re already using a supported browser, you can refresh your screen and try again to sign in.

        That's why a workaround need's to be used. You can access gmail when you log into the google account from
        stackoverflow.com and then go to gmail.com
        """

        # Visit stackoverflow.com log in page.
        driver.get("https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f")
        time.sleep(2)

        # Click "Log in with Google" button.
        driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        time.sleep(2)

        # Enter Username into input field.
        driver.find_element_by_xpath('//input[@type="email"]').send_keys(credentials['Login'])
        time.sleep(2)

        # Click "Next" button.
        driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        time.sleep(2)

        # Enter Password into input field.
        driver.find_element_by_xpath('//input[@type="password"]').send_keys(credentials['Password'])
        time.sleep(2)

        # Click "Next" button.
        driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        time.sleep(2)

        # Finally, redirect to gmail.com
        driver.get("https://gmail.com")
        time.sleep(2)
