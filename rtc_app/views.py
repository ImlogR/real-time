from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GroupModel, ChatModel, Transaction, Coin
from django.contrib import messages
from django.utils.text import slugify
from authentication.models import CustomUser
# Create your views here.

def index(request):
    groups= GroupModel.objects.all()
    # coins= Coin.objects.filter(owner= request.user)
    # if request.user.is_authenticated:
        # receivers= CustomUser.objects.exclude(email= request.user.email)
    # else:
        # receivers= CustomUser.objects.all()
    if request.method== 'POST':
        group_name= request.POST['group_name']
        group_slug= slugify(request.POST['group_name'])
        if GroupModel.objects.filter(slug=group_slug).exists():
            messages.info(request, "Group with this name already exists!")
            return redirect('/')
        else:
            # group= GroupModel.objects.filter(name= group_name).first()
            group= GroupModel(name= group_name, slug= group_slug)
            group.save()
            return redirect('/'+ group_slug + '/')


    else:
        # return render(request, "rtc_app/index.html", {'groups': groups, 'coins':coins, 'receivers':receivers})
        return render(request, "rtc_app/index.html", {'groups': groups})

def lobby(request, group_name):
    group_slug= slugify(group_name)
    group= GroupModel.objects.filter(slug=group_slug).first()
    
    chats= []
    
    if group:
        chats= ChatModel.objects.filter(group= group)
    else:
        return redirect('/')

    return render(request, "rtc_app/lobby.html", {'group_name': group.name, 'chats': chats})

@login_required
def profile(request):
    profile_detail= CustomUser.objects.get(email= request.user.email)
    coin_details= Coin.objects.filter(owner= profile_detail)
    transaction_details= Transaction.objects.filter(sender= profile_detail)
    # dd(coin_details)
    # print(coin_details)
    # print(transaction_details)
    # dd(profile_detail)
    context= {
        'profile':profile_detail,
        'coins':coin_details,
        'transactions':transaction_details,
    }
    return render(request, 'rtc_app/profile.html', context)

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'rtc_app/index.html', {'transactions': transactions})
