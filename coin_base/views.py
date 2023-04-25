from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CoinUserProfile, Transaction, Coin
from rtc_app.models import ChatModel

# @login_required
# def send_message(request, receiver_id):
#     sender_profile = UserProfile.objects.get(user=request.user)
#     receiver_profile = UserProfile.objects.get(id=receiver_id)
#     coins = 10 # or any other value

#     # Create a new transaction object
#     transaction = Transaction.objects.create(sender=sender_profile, receiver=receiver_profile, coins=coins)

#     # Update the sender and receiver's coin balance
#     sender_profile.coins -= coins
#     sender_profile.save()
#     receiver_profile.coins += coins
#     receiver_profile.save()

#     return redirect('inbox')

def create_coins(request, owner):
    user= request.user.first_name
    messages= ChatModel.objects.filter(sent_by= owner)
    if messages.count() >= 5:
        coin= Coin.objects.create(
            owner= owner,
            amount= 10
        )
        coin.save();


# def give_coins(sender, receiver):
#     coin= Coin.objects.get(owner= sender)
#     transaction= Transaction.objects.create(sender, receiver, coin)
#     transaction.save();