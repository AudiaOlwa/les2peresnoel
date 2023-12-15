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
    path("livre/<int:livre_id>/", views.livre, name="livre_detail"),
    path("musique/<int:musik_id>/", views.musique, name="musique_detail"),
    path("video/<int:video_id>/", views.video, name="video_detail"),
    path("signup", views.signup, name="signup"),
    path("evolution", views.evolution, name="evolution"),
    path("prqw2pn", views.prqw2pn, name="prqw2pn"),
    path("birth", views.birth, name="birth"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)