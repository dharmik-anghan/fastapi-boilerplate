import os
import smtplib 
from email.message import EmailMessage
from random import randint

def generate_OTP():
    return randint(100000 , 999999)


def send_otp_email(to_email, otp):
    from_email = os.getenv("from_email")
    email_password = os.getenv("email_password")

    subject = "Your OTP"
    body = f"Your Verification OTP is : {otp}"

    try:
        # Create an EmailMessage object
        message = EmailMessage()
        message.set_content(body)
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email

        # Establish the SMTP connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, email_password)

            # Send the email message
            server.send_message(message)

        return {"message" : "Email sent successfully"}

    except smtplib.SMTPException as e:
        print(f"Error sending email: {str(e)}")