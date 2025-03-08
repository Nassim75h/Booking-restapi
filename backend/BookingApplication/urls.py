
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/",include('debug_toolbar.urls')),

    # verification-related routes (activation and password reset confirmation...etc) without any prefix
    path('', include('authapp.verification_via_email.urls')),
    path("api/v0/", include([
        path("admin/", include("adminapp.urls")),
        path("auth/", include("authapp.urls")),
        path("booking/", include("booking.urls")),
    ])),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
