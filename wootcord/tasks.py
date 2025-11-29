from celery import Celery
from .config import broker_url

queue = Celery('task_queue', broker=broker_url)

queue.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)