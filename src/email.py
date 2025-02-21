import smtplib
from email.mime.text import MIMEText
from typing import NoReturn
from .config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

def send_confirmation_email(to_email: str, appointment_info: str) -> NoReturn:
    body = (
        f"hello,\n\n"
        f"this is to confirm your appointment:\n{appointment_info}\n\n"
        f"cheers,\nvoice ai receptionist"
    )
    msg = MIMEText(body)
    msg["subject"] = "appointment confirmation"
    msg["from"] = EMAIL_USER
    msg["to"] = to_email

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("confirmation email sent")
    except Exception as e:
        print("error sending email:", e)
