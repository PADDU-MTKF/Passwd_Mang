from dotenv import load_dotenv
import os
from email.message import EmailMessage
import ssl
import smtplib


def send_email(body, subject='OTP VERIFICATION'):

    load_dotenv()
    FROM_EMAIL = os.getenv('FROM_EMAIL')
    PASWD = os.getenv('MAIL_PASS')
    TO_EMAIL = os.getenv('TO_EMAIL')

    em = EmailMessage()
    em['From'] = FROM_EMAIL
    em['To'] = TO_EMAIL
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(FROM_EMAIL, PASWD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, em.as_string())


#send_email('Use 123456 as your OTP','OTP VERIFICATION')
