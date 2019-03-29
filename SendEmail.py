import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from JsonFileManager import ToolSetSettingsJson


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

    def server_quit(self):
        if self.__if_login:
            self.__server.quit()
            self.__if_login = False

    def __attach_file(self, file_path):
        file = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " +
                        os.path.basename(file_path))
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


def ask_user_for_files_gui(title='Choose files'):

    # import tkinter
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()  # get rid of tkinter default window
    files = filedialog.askopenfilenames(parent=root, title=title)
    return root.tk.splitlist(files)


if __name__ == "__main__":

    # importing console functions
    import ConsoleFunctions
    console = ConsoleFunctions.ConsolePrintFunctions()
    console.print_one_line_title("Email Sender // Created by @RealA10N", "single heavy square")
    print()  # to go down one line

    # let user select files
    console.print_replaceable_line('Please select all the files you want to attach your email')
    files_list = ask_user_for_files_gui()

    files_string = ''
    for file in files_list:
        files_string = files_string + str(os.path.basename(file)) + ', '
    files_string = files_string[0:-2]  # remove the last ', '

    console.print_replaceable_line('The Selected files are: ')
    print(files_string)

    # load info from 'ToolSetSettings' file
    json_settings = ToolSetSettingsJson()

    email = SendEmail()
    email.add_recipient_address(json_settings.get_addressee_email())
    email.set_subject('Here are your files!')
    email.add_body('Sent automatically by a bot. Created by @RealA10N')

    # add all the files to the email
    for file in files_list:
        email.add_file(file)

    console.print_replaceable_line('Connecting to google servers...')
    email.login(json_settings.get_sender_email, json_settings.get_sender_password())
    email.send_mail()
    email.server_quit()
    console.print_replaceable_line('Email sent successfully!')
