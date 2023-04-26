from django.shortcuts import render, redirect
from .models import GroupModel, ChatModel, Transaction, Coin
from django.contrib import messages
from django.utils.text import slugify
from authentication.models import CustomUser
# Create your views here.

def index(request):
    groups= GroupModel.objects.all()
    coins= Coin.objects.filter(owner= request.user)
    receivers= CustomUser.objects.exclude(email= request.user.email)
    if request.method== 'POST':
        group_name= slugify(request.POST['group_name'])
        if GroupModel.objects.filter(name=group_name).exists():
            messages.info(request, "Group with this name already exists!")
            return redirect('/')
        else:
            # group= GroupModel.objects.filter(name= group_name).first()
            group= GroupModel(name= group_name)
            group.save()
            return redirect('/'+ group_name + '/')


    else:
        return render(request, "rtc_app/index.html", {'groups': groups, 'coins':coins, 'receivers':receivers})

def lobby(request, group_name):
    group_name= slugify(group_name)
    group= GroupModel.objects.filter(group_id=group_name).first()
    
    chats= []
    
    if group:
        chats= ChatModel.objects.filter(group= group)
    else:
        return redirect('/')

    return render(request, "rtc_app/lobby.html", {'group_name': group_name, 'chats': chats})

def profile(request):
    return render(request, 'rtc_app/profile.html')

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'rtc_app/index.html', {'transactions': transactions})
