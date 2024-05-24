import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def SendEmail(receiver_email, Subject, body):
    sender_email = 'sklenicka.filip@gmail.com'
    app_password = "vvgi uzbr uyvo hglv"
    # S tim heslem nic neudelas je to app password ne moje heslo xDDDDD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = Subject
    body = body
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email odeslan!")
    except Exception as e:
        print(f"Error: {e}")
