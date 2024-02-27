from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.consumers import GraphConsumer
'''
application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/index/", GraphConsumer.as_asgi()),
        ]
    ),
})
'''