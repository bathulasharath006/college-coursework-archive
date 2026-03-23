import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime as dt
import os

# Read these from config
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "admin@test.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))
    
    if "Monthly Library Report" in subject:
        # Attach PDF
        pdf_path = os.path.join(
              os.path.abspath(os.path.dirname(__file__)),
              "../db_directory/Monthly_Reports/",
              f"Monthly_Report_{dt.today().strftime('%Y_%m_%d')}.pdf" )

        with open(pdf_path, "rb") as pdf_file:
            part = MIMEApplication(pdf_file.read(),
            Name=f"Monthly_Report_{dt.today().strftime('%Y_%m_%d')}.pdf")
        part['Content-Disposition'] = f'attachment; filename="Monthly_Report_{dt.today().strftime("%Y_%m_%d")}.pdf"'
        msg.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    
    return True
