from .models import Coin, Transaction, ChatModel
from authentication.models import CustomUser
import hashlib
import json

def create_coin(self,owner):
    message_count= ChatModel.objects.filter(sent_by= owner).count()
    coin_owner= CustomUser.objects.get(first_name= owner)
    if message_count % 10 == 0:
        # previous_coin= Coin.objects.last()
        # coin.prev_coin= previous_coin
        # last_coin= Coin.objects.last()
        last_coin = Coin.objects.order_by('-created_at').first()
        if last_coin:
            coin= Coin.objects.create(owner= coin_owner)
            coin.prev_coin= last_coin
            # coin.save();
            last_coin.next_coin= coin
            last_coin.save();
        else:
            coin=Coin.objects.create(owner= coin_owner)

        coin.next_coin= None
        coin.save();
        self.send_json({
            'type': 'websocket.send',
            'message': {"message": "Hooray, you owned a Laplace " + str(coin.coin_id) + " !!", "user": "ChatAdmin"}
        })

        transaction = Transaction.objects.create(sender=None, receiver=coin_owner, coin=coin, amount=1)
        transaction.save()

def transaction_trigger(sender, receiver, coin):
    coin= Coin.objects.get(coin_id= coin)
    if sender== coin.owner:
        last_transaction= Transaction.objects.filter(coin= coin).order_by('-created_at').first()
        if last_transaction:
            new_transaction= Transaction(sender= last_transaction.receiver, receiver= receiver, coin= coin, amount= 1)
            new_transaction.prev_transaction= last_transaction
            new_transaction.next_transaction= None
            last_transaction.next_transaction= new_transaction

def create_transaction(sender,receiver, coin):
    coin= Coin.objects.get(coin_id= coin)
    receiver= CustomUser.objects.get(email= receiver)
    if sender== coin.owner:
        last_transaction= Transaction.objects.filter(coin= coin).order_by('-created_at').first()
        if last_transaction:
            new_transaction= Transaction(sender= coin.owner, receiver= receiver, coin= coin, amount= 1)
            new_transaction.prev_transaction= last_transaction
            new_transaction.next_transaction= None
            new_transaction.save()
            last_transaction.next_transaction= new_transaction
            last_transaction.save()
            coin.owner= receiver
            coin.save()

def get_coin_data(owner):
    owns= CustomUser.objects.get(email= owner)
    coin = Coin.objects.filter(owner=owns).first()
    return coin;

# def get_coin_data(owner, all):
#     owns= CustomUser.objects.get(email= owner)
#     coin = Coin.objects.filter(owner=owns)
#     return coin;

def syn_get_coin_data(owner):
    coins = Coin.objects.filter(owner= owner).values()
    print(coins)
    coin_list = []
    for coin in coins:
        # print(coin)
        coin_dict = {
            'coin_id': str(coin['coin_id']),
            'owner-id': str(coin['owner_id']),
            'created_at': str(coin['created_at']),
            'hash': coin['hash'],
            'prev_coin': str(coin['prev_coin_id']) if coin['prev_coin_id'] else None,
            'next_coin': str(coin['next_coin_id']) if coin['next_coin_id'] else None,
        }
        coin_list.append(coin_dict)
    return coin_list

def tran_data_to_send():
    latest_transaction= Transaction.objects.all().order_by('-created_at').first()
    print('sent transaction', latest_transaction.pk)
    owner= latest_transaction.receiver
    transaction= { 
        'created_at':str(latest_transaction.created_at),
        'owner': str(owner),
        'previous_hash':str(latest_transaction.prev_transaction.hash) if latest_transaction.prev_transaction else None,
        # 'random_number': str(random.randint(9999,999999))
        }
    
    return transaction