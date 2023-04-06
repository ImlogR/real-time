from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'messages', 'timestamp', 'group']
    
@admin.register(GroupModel)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'name']
