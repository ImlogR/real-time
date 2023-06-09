from django.urls import re_path
from . import consumers


websocket_urlpatterns= [
    re_path(fr'^ws/socket-server/room/(?P<group_name>[-\w]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(fr'^ws/socket-server/laplace-socket/$', consumers.LaplaceConsumer.as_asgi()),
    re_path(fr'^ws/socket-server/data-socket/$', consumers.dataConsumer.as_asgi()),
    re_path(fr'^ws/a-socket-server/(?P<group_name>[-\w]+)/$', consumers.AsyncChatConsumer.as_asgi()),
]