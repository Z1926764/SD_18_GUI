from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.consumers import GraphConsumer

'''
websocket_urlpatters = [
    re_path(r"ws/index/$"), consumers.GraphConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/index/", GraphConsumer.as_asgi()),
        ]
    ),
})
'''