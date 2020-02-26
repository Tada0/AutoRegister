from selenium.webdriver import Chrome
from typing import List
import time


class MailHandler:
    @staticmethod
    def read_mail(driver: Chrome, mail_id: str):
        # Navigate the target mail and open it
        driver.find_element_by_xpath(f'//tr[@aria-labelledby="{mail_id}"]').click()
        time.sleep(2)

    @staticmethod
    def download_attachment(driver: Chrome):
        # Find the attachment download button and click it
        driver.find_element_by_xpath(f'//div[@class="T-I J-J5-Ji aQv T-I-ax7 L3"]').click()
        time.sleep(2)

    @staticmethod
    def return_to_mail_list(driver: Chrome):
        # Navigate the "Inbox" button and click it
        driver.find_element_by_xpath('//a[@class="J-Ke n0"]').click()
        time.sleep(2)

    @staticmethod
    def fetch_all_xlsx_files(driver: Chrome, mail_ids: List[str]):
        for unread_email_id in mail_ids:
            MailHandler.read_mail(driver, unread_email_id)
            MailHandler.download_attachment(driver)
            MailHandler.return_to_mail_list(driver)
