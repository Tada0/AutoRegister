from selenium.webdriver import Chrome
from typing import List
from bs4 import BeautifulSoup


class FindUnreadEmails:
    @staticmethod
    def execute(driver: Chrome, email_from: str) -> List[str]:
        """
        Gmail page is created dynamically with javascript

        Once a page is modified by ajax requests, the current HTML exists only inside the browser's DOM.
        There's no longer any independent source HTML that you can validate other than what you can pull out of the DOM.

        That's why using driver.page_source won't give you the actual html -> we need to get the
        WebElement object of <html> tag and get it's inner html.
        """

        page_source = driver.find_element_by_xpath('//html[@class="aAX"]').get_attribute('innerHTML')

        soup = BeautifulSoup(page_source, features='html.parser')

        # Selecting only unread ones -> read ones are "zA y0" class
        # Also additional "byw" class means there is an attachment -> only selecting those.
        mails = soup.find_all('tr', {"class": "zA zE byw"})

        # Selecting those that are sent from right mail
        return [mail['aria-labelledby'] for mail in mails if mail.find("span", {"class": "zF"})['email'] == email_from]
