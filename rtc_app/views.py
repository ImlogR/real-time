from django.shortcuts import render
from .models import GroupModel, ChatModel

# Create your views here.

def lobby(request, group_name):
    group= GroupModel.objects.filter(name= group_name).first()
    chats= []
    
    if group:
        chats= ChatModel.objects.filter(group= group)

    else:
        group= GroupModel(name= group_name)
        group.save();

    return render(request, "rtc_app/lobby.html", {'group_name': group_name, 'chats': chats})