# from django.contrib import admin
from baton.autodiscover import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from les2peresnoel import core

urlpatterns = [
    path("admin/", admin.site.urls),
    path("baton/", include("baton.urls")),
    path("", include("les2peresnoel.core.urls")),
    path("accounts/", include("allauth.urls")),
    # path("core/", include("les2peresnoel.core.urls")),
    path("marketplace/", include("les2peresnoel.marketplace.urls")),
    path("stores/", include("les2peresnoel.stores.urls")),
    path("providers/", include("les2peresnoel.providers.urls")),
    path("payments/", include("les2peresnoel.payments.urls")),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path("login/", core.views.login, name="login"),
    path("licences/", include("les2peresnoel.licences.urls")),
]


# if settings.DEBUG:
if True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
