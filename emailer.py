import smtplib
from variables import*

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_address, subject, body):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_CREDENTIALS)

    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_address
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))
    server.sendmail(EMAIL_ADDRESS, receiver_address, message.as_string())

    server.quit()
