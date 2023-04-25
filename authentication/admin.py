from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'is_superuser']