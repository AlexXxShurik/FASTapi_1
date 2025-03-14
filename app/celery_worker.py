from celery import Celery
from dotenv import load_dotenv
import os


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

@celery.task
def send_report_task(email: str):
    """
    Задача для отправки отчёта на email.
    В данном примере просто логируем сообщение в консоль.
    """
    print(f"Report sent to {email}")
    return {"status": "success", "email": email}