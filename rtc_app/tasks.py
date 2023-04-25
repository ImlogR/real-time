from celery import shared_task
from rtc_app.models import ChatModel

@shared_task
def flush_chat_database():
    ChatModel.objects.all().delete()
