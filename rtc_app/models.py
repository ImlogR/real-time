from django.db import models
import uuid
# Create your models here.
class GroupModel(models.Model):
    group_id= models.UUIDField(primary_key=True, default= uuid.uuid4)
    name= models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ChatModel(models.Model):
    chat_id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    messages= models.CharField(max_length=1000)
    timestamp= models.DateTimeField(auto_now_add=True)
    group= models.ForeignKey(GroupModel, related_name='group_chats', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.messages

