import json
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *

from .filtration import word_filter, simi_percentage

from .spam_detection import spammer

from .coin import create_coin, get_coin_data, syn_get_coin_data, tran_data_to_send, transaction_trigger, create_transaction

from channels.db import database_sync_to_async

from asgiref.sync import sync_to_async
import random

class dataConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "laplace",
            self.channel_name,
        )

    def receive_json(self, content, **kwargs):
        print('message received data', content)
        last_transaction= Transaction.objects.filter(coin= content['coin']).order_by('-created_at').first()
        last_hash= last_transaction.hash
        print(last_hash)
        content['prev_hash']= last_hash
        content['random']= random.randint(9999, 999999)
        async_to_sync(self.channel_layer.group_send)(
            "laplace",
            {
                'type': 'data.content',
                'laplace': content,
            }
        )
        # self.close()
        # self.connect()

    def data_content(self, event):
        self.send_json(
            {
                'laplace': event['laplace']
            }        
        )

    def disconnect(self, code):
        print('disconnected', code)


hash_list= []
content_list= []
class LaplaceConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.update_coin_data()
        # coin_data= syn_get_coin_data(self.scope['user'])
        # self.send_json({
        #     'type': 'websocket.send',
        #     'coins': coin_data
        # })
        print(' sync laplace connected')

    def receive_json(self, content, **kwargs):
        print('message received laplace', content)
        hash_list.append(content['hash'])
        content_list.append(content)
        # print("Content list",content_list)
        grouped_data= {}
        for item in content_list:
            coin= item['coin']
            hash= item['hash']
            if coin in grouped_data:
                grouped_data[coin].append(hash)
            else:
                grouped_data[coin]= [hash]
        print('grouped data ',grouped_data)
        print("hash values",grouped_data[content['coin']])
        print('similarity', simi_percentage(hash_values=grouped_data[content['coin']]))
        if simi_percentage(hash_values=grouped_data[content['coin']]) > 50:
            create_transaction(self.scope['user'], content['receiver'], content['coin'])
            coin_updated= syn_get_coin_data(self.scope['user'])
            self.send_json({
                'type':'websocket.send',
                # 'message': {"message": "transaction successful!!"}
                'coins': coin_updated,
                'message':{"message":"transaction Successful!"}
            })


    def disconnect(self, code):
        content_list.clear()
        print('disconnected', code)

    def update_coin_data(self):
        coin_data= syn_get_coin_data(self.scope['user'])
        self.send_json({
            'type': 'websocket.send',
            'coins': coin_data
        })

class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_name= self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        print('connection established')
    
    def receive_json(self, content, **kwargs):
        print('message received', content)

        group= GroupModel.objects.get(name= self.group_name)
        if self.scope['user'].is_authenticated:
            print("coin data", get_coin_data(self.scope['user'].email))
            if not spammer(self.scope['user'].first_name):
                chat= ChatModel(
                    sent_by= self.scope['user'].first_name,
                    messages= word_filter(content['message']),
                    group= group
                )
                chat.save();
                create_coin(self, self.scope['user'].first_name)

                print(spammer(self.scope['user'].first_name))

                content['user']= self.scope['user'].first_name
                content['message']= word_filter(content['message'])
                # print(content)
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        'type': 'chat.message',
                        'message': content,
                    }
                )
            else:
                self.send_json({
                    'type': 'websocket.send',
                    'message': {"message": "You spammer piece of shit!!", "user": "ChatAdmin"}
                })
        else:
            self.send_json({
                'type': 'websocket.send',
                'message': {"message": "You should login to send messages!!", "user": "Anonymous"}
            })
    
    def chat_message(self, event):
        self.send_json(
            {
                'message': event['message']
            }        
        )

    def disconnect(self, code):
        # print('disconected', code)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        # raise StopConsumer()



class AsyncChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('connected')
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print('message received', content)
        await self.send_json(content)

    async def disconnect(self, code):
        print('disconnected', code)