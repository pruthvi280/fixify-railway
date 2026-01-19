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


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "noreply.fixify.com@gmail.com"  # Replace with your Gmail
SENDER_PASSWORD = "pkvo qeio izlf npqa"  # Use App Password if 2FA is enabled

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

