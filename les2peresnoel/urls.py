from django.conf import settings
from django.conf.urls.static import static
from core import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("boutique", views.boutique, name="boutique"),
    path("livre", views.livre, name="livre"),
    path("musique", views.musique, name="musique"),
    path("video", views.video, name="video"),
    path("signup", views.signup, name="signup"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)