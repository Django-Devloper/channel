"""
url router for websocket connection
"""

from django.urls import path
from .consumers import YourCustomConsumerName

websocket_patterns = [
    path("path/<str:group_name>/", YourCustomConsumerName.as_asgi()),
]
