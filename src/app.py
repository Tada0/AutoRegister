from src.common import WrongNumberOfKeysError, WrongParameterTypeError
from src.selenium.GmailHandler.Login import Login
from src.selenium.GmailHandler.Find_Unread_Emails import FindUnreadEmails
from src.selenium.GmailHandler.GmailHandler import GmailHandler
from src.selenium.RegisterHandler.Register import Register
from src.selenium.common import DriverCommon
from src.xlsx.XLSXHandler import XLSXHandler
from src.common import FileHandler, HashableDict
from src.mail.MailSender import MailSender
from typing import Dict
import argparse
import time
import json
import os


class App:
    def __init__(self, options: Dict[str, str or bool]):
        self.options = options

    def run(self):
        driver_options = DriverCommon.prepare_chrome_options(
            self.options['headless'],
            self.options['working_directory']
        )

        driver = DriverCommon.create_driver("../Driver/chromedriver.exe", driver_options)
        Login.execute(driver, {
            'Login': self.options['gmail_account_name'],
            'Password': self.options['gmail_account_password']
        })

        while True:
            if unread_mails := FindUnreadEmails.execute(driver, self.options['sender_email']):
                GmailHandler.fetch_all_xlsx_files(driver, unread_mails)

                valid_files, not_valid_files = XLSXHandler.validate_files(self.options['working_directory'])
                valid_users, not_valid_users = XLSXHandler.fetch_new_users(valid_files)

                DriverCommon.open_new_tab(driver, self.options['registration_website'])

                registration_statuses = {
                    HashableDict(user): Register.execute(driver, user) for user in valid_users
                }

                DriverCommon.close_current_tab(driver)

                MailSender(MailSender.create_mail(
                    registration_statuses, XLSXHandler.filter_empty_rows(not_valid_users), not_valid_files
                )).send(
                    self.options['gmail_account_name'],
                    self.options['gmail_account_password'],
                    self.options['sender_email']
                )

                FileHandler.clear_directory(self.options['working_directory'])

            time.sleep(30)

            GmailHandler.refresh(driver)


def parse_arguments() -> Dict[str, str or bool]:
    def validate(config_path: str):

        required_keys = {
            "gmail_account_name": str,
            "gmail_account_password": str,
            "working_directory": str,
            "sender_email": str,
            "registration_website": str,
            "headless": bool
        }

        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            if config.keys() != required_keys.keys():
                raise WrongNumberOfKeysError(
                    f"Config file consists of wrong keys! The keys should be:\n{', '.join(required_keys)}"
                )
            for key, key_type in required_keys.items():
                if type(config[key]) != key_type:
                    raise WrongParameterTypeError(key, type(config[key]), key_type)
        except FileNotFoundError as error:
            print(f"{error}\nGiven config file does not exist!")
        except json.decoder.JSONDecodeError:
            print("Given config file is not a valid json format.")
        except WrongNumberOfKeysError as error:
            print(error.message)
        except WrongParameterTypeError as error:
            print(error.message)
        else:
            return
        os._exit(1)

    def fetch_config(config_path: str) -> Dict[str, str or bool]:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--config_path", metavar="<config>", required=True, help="Path to the config file")
    config_path = vars(parser.parse_args())['config_path']
    validate(config_path)
    return fetch_config(config_path)


if __name__ == '__main__':
    app = App(parse_arguments())
    app.run()
