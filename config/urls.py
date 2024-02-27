from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from les2peresnoel import core

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("les2peresnoel.core.urls")),
    # path("core/", include("les2peresnoel.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
