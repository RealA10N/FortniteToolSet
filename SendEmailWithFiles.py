import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def SendEmail(user_email, user_password, send_email_to, subject='No Subject', body='', attchments=None):

    # define email variables
    msg = MIMEMultipart()
    msg['Form'] = user_email
    msg['To'] = send_email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    send_text = msg.as_string()

    # connect to google servers
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user_email, user_password)

    # send email and quit
    server.sendmail(user_email, send_email_to, send_text)
    server.quit()


user_email = input('enter email username: ')
user_password = input('enter email password: ')
send_email_to = input('enter how you want to send the email to: ')
SendEmail(user_email, user_password, send_email_to, 'this is my subject!', 'and this is the body')
