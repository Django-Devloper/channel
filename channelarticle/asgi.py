"""
asgi.py file is a key component when adding asynchronous capabilities to a Django project using ASGI (Asynchronous Server Gateway Interface).

"""
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import channelarticle.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channelarticle.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(channelarticle.routing.websocket_patterns)
        ),
    }
)
