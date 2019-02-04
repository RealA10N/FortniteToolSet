import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class SendEmail:

    def __init__(self):
        self.__user_email = None
        self.__user_password = None
        self.__recipients_email = []
        self.__attachments = []
        self.__if_login = False

        self.__msg = MIMEMultipart()
        self.__server = None

    def set_subject(self, subject):
        self.__msg['Subject'] = subject

    def add_body(self, body):
        self.__msg.attach(MIMEText(body, 'plain'))

    def add_file(self, file_path):
        self.__attachments.append(file_path)

    def clear_files(self):
        self.__attachments = []

    def add_recipient_address(self, email):
        self.__recipients_email.append(email)

    def clear_recipients(self):
        self.__recipients_email = []

    def login(self, user_email, user_password):

        self.__user_email = user_email
        self.__user_password = user_password

        # logging to gmail servers
        self.__server = smtplib.SMTP('smtp.gmail.com', 587)
        self.__server.starttls()
        self.__server.login(user_email, user_password)

        self.__if_login = True

    def __attach_file(self, file_path):
        file = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + os.path.basename(file_path))
        return part

    def send_mail(self):

        # check if logged to server
        if not self.__if_login:
            raise Exception('You must login first')

        # check if at least one recipient
        if self.__recipients_email == []:
            raise Exception('Please add a least one recipient')

        # attach email details to msg
        self.__msg['Form'] = self.__user_email
        self.__msg['To'] = ", ".join(self.__recipients_email)

        # attach files to msg
        for file in self.__attachments:
            part = self.__attach_file(file)
            self.__msg.attach(part)

        # sending the email
        send_body = self.__msg.as_string()
        self.__server.sendmail(self.__user_email, self.__recipients_email, send_body)
        self.__server.quit()

