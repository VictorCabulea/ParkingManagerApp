import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


def send_email(email_receiver: str, subject: str, body: str):
    email_sender = "victorandy1999@gmail.com"

    load_dotenv()
    email_password = os.environ.get("EMAIL_PASSWORD")

    if email_password is None:
        print("EMAIL_PASSWORD environment variable is not set.")
        return

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(email_sender, email_password)
            server.send_message(em)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")