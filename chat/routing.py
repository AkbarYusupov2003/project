from django.urls import path

from chat import consumers


websocket_urlpatterns = [
    path("chat/<uuid:uuid>/", consumers.ChatConsumer.as_asgi()),
]
