import os

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()
#for channels####
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import rtc_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_chat.settings')

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rtc_app.routing.websocket_urlpatterns
        )
    )
})
