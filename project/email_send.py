import smtplib
from email.mime.text import MIMEText


def send_email(message, mail):
    sender = 'arthouserooms@gmail.com'
    with open('password.txt') as file:
        for i in file.readlines():
            password = i

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message, "html")
        msg["From"] = sender
        msg["To"] = mail
        msg["Subject"] = 'Подтверждение бронирования'
        server.sendmail(sender, mail, msg.as_string())
    except Exception:
        pass


