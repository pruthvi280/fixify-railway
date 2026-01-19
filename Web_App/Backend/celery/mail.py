# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# SMTP_SERVER="localhost"
# SMTP_PORT="1025"
# SENDER_EMAIL="fixify@.com"
# SENDER_PASSWORD=""


# def send_mail(to,subject,content):

#   msg=MIMEMultipart()
#   msg['To']=to
#   msg['Subject']=subject
#   msg['From']=SENDER_EMAIL

#   msg.attach(MIMEText(content,'html'))

#   with smtplib.SMTP(host=SMTP_SERVER,port=SMTP_PORT) as client:
#     client.send_message(msg)
#     client.quit()

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("MAIL_PORT", 587))
SENDER_EMAIL = os.getenv("MAIL_USERNAME")
SENDER_PASSWORD = os.getenv("MAIL_PASSWORD")

def send_mail(to, subject, content):
    msg = MIMEMultipart()
    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg.attach(MIMEText(content, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as client:
            client.starttls()  # Secure the connection
            client.login(SENDER_EMAIL, SENDER_PASSWORD)
            client.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

