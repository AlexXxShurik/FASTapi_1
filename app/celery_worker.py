from celery import Celery
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

celery = Celery(
    __name__,
    broker=os.getenv("BROKER_URL"),
    backend=os.getenv("RESULT_BACKEND")
)

celery.conf.update(
    result_expires=3600,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

sender_email = "gmail@gmail.com"
password = "password1234"

subject = "Тема письма"
body = "Это тестовое сообщение."

message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

@celery.task
def send_report_task(email: str):
    """
    Задача для отправки отчёта на email.
    """
    message["To"] = email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, email, message.as_string())
        print("Письмо успешно отправлено!")
        return "success"
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return "error"
