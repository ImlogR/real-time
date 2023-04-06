import json
# from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("connection open or established", event)
        print("channel layer", self.channel_name)
        self.group_name= self.scope['url_route']['kwargs']['group_name']
        print('group name', self.group_name)
        async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name)

        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self, event):
        text_data_json= json.loads(event['text'])
        message= text_data_json['message']
        print(message)
        group= GroupModel.objects.get(name= self.group_name)
        
        if self.scope['user'].is_authenticated:
            chat= ChatModel(
                messages= message,
                group= group
            )
            chat.save();
            text_data_json['user']= self.scope['user'].username
            async_to_sync(self.channel_layer.group_send)(self.group_name,{
                'type':'chat.message',
                'message': json.dumps(text_data_json)
                # 'message': event['text']
            })
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"message": "login required!", "user": "Anonymous"})
            })
            

    
    def chat_message(self, event):
        print(event)
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })
        # self.send({
        #     'type':'websocket.send',
        #     'text': json.dumps({"message": message})
        # })
        # print("received message:", event['text'])
        # for i in range(50):
        #     self.send({
        #         'type':'websocket.send',
        #         'text': json.dumps({"count": i+1})
        #     })
        #     sleep(1)

    def websocket_disconnect(self, event):
        print("disconnected!", event)
        print("channel layer", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        raise StopConsumer()


class AsyncChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connection open or established", event)
        print("channel layer", self.channel_name)
        self.group_name= self.scope['url_route']['kwargs']['group_name']
        print('group name', self.group_name)
        await self.channel_layer.group_add(
                self.group_name,
                self.channel_name)

        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
        text_data_json= json.loads(event['text'])
        message= text_data_json['message']
        print(message)
        group= await database_sync_to_async(GroupModel.objects.get)(name= self.group_name)

        chat= ChatModel(
            messages= message,
            group= group
        )
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(self.group_name,{
            'type':'chat.message',
            'message': event['text']
        })
    
    async def chat_message(self, event):
        print(event)
        await self.send({
            'type':'websocket.send',
            'text': event['message']
        })
        # self.send({
        #     'type':'websocket.send',
        #     'text': json.dumps({"message": message})
        # })
        # print("received message:", event['text'])
        # for i in range(50):
        #     self.send({
        #         'type':'websocket.send',
        #         'text': json.dumps({"count": i+1})
        #     })
        #     sleep(1)

    async def websocket_disconnect(self, event):
        print("disconnected!", event)
        print("channel layer", self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         self.send(text_data=json.dumps({
#             'type':'connected to the socket!!',
#             'message':'You are in!!'
#         }))
        # return super().connect()
    
    # def receive(self, text_data=None, bytes_data=None):
    #     return super().receive(text_data, bytes_data)
    
    # def disconnect(self, code):
    #     return super().disconnect(code)