import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookingApplication.settings.dev')

print("ASGI application is starting...")  # Debugging line
#next time leave the imports after the below lunch

django_asgi_app = get_asgi_application()


from booking.middleware import JWTAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from booking.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
    ),
})
