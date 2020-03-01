from typing import List, Dict
import datetime
import smtplib


class Mail:
    def __init__(self, content: str):
        self.content = content
        self.title = "Registration Report"


class MailSender:
    def __init__(self, mail: Mail):
        self.mail = mail

    @staticmethod
    def create_mail(registration_statuses: Dict, not_valid_users: List, not_valid_files: List) -> Mail:
        successes = [
            (user, status) for user, status in registration_statuses.items() if status == 'User Registered Successfully'
        ]
        failures = [status for status in registration_statuses.items() if status not in successes]
        NEW_LINE = '\n'
        return Mail(NEW_LINE.join([line.strip() for line in f"""
        Successfully Registered Users:
        {NEW_LINE.join([f"{user['name']} {user['surname']}, {user['email']}" for user, status in successes])}

        Registration Failures:
        {NEW_LINE.join([f"{user['name']} {user['surname']}, {user['email']} - {status}" for user, status in failures])}

        Invalid User Information (Some information might be missing (can be password - not shown here)):
        {NEW_LINE.join([f"{user['name']} {user['surname']}, {user['email']}, {user['phone number']}" for user in not_valid_users])} 

        Invalid Files Found (Wrong format / Wrong columns):
        {NEW_LINE.join(not_valid_files)}
        """.strip().split('\n')]))

    def send(self, email: str, password: str, addressee: str):
        conf = {
            'host': "smtp.gmail.com",
            'port': 465,
            'tls': True,
            'username': email,
            'password': password,
            'sender': addressee,
        }

        headers = {
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Disposition': 'inline',
            'Content-Transfer-Encoding': '8bit',
            'From': email,
            'To': addressee,
            'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
            'X-Mailer': 'python',
            'Subject': self.mail.title
        }

        mailer = smtplib.SMTP_SSL(conf['host'], conf['port'])
        mailer.ehlo()
        mailer.login(conf['username'], conf['password'])
        mailer.sendmail(headers['From'], addressee, "Subject: {}\n\n{}".format(headers['Subject'], self.mail.content).encode("utf8"))
        mailer.quit()

