import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def __attach_file(file_path):
    file = open(file_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + file_path)
    return part


def send_email(user_email, user_password, recipient, subject=None, body=None, attchments=None):

    msg = MIMEMultipart()

    # attach email details to msg
    msg['Form'] = user_email
    msg['To'] = recipient

    # add subject
    if subject is not None:
        msg['Subject'] = subject

    # add body
    if body is not None:
        msg.attach(MIMEText(body, 'plain'))

    # attach files to msg
    if attchments is not None:
        if type(attchments) is list:
            for file in attchments:
                part = __attach_file(file)
                msg.attach(part)
        elif type(attchments) is str:
            part = __attach_file(attchments)
            msg.attach(part)

    # connect to google servers
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user_email, user_password)

    # send email and quit
    send_text = msg.as_string()
    server.sendmail(user_email, recipient, send_text)
    server.quit()
