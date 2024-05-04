# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

django_asgi_app = get_asgi_application()


import server.Web.routing as web


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        web.routing.websocket_urlpatterns
    ),
})