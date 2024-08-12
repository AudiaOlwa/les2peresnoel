from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("boutique", views.boutique, name="boutique"),
    path("legend_rebirth", views.legend_rebirth, name="legend_rebirth"),
    path("sage", views.sage, name="sage"),
    path("livre/<int:livre_id>/", views.livre, name="livre_detail"),
    path("musique/<int:musik_id>/", views.musique, name="musique_detail"),
    path("video/<int:video_id>/", views.video, name="video_detail"),
    path("signup", views.signup, name="signup"),
    path("evolution", views.evolution, name="evolution"),
    path("prqw2pn", views.prqw2pn, name="prqw2pn"),
    path("birth", views.birth, name="birth"),
    path("gallerie", views.gallerie, name="gallerie"),
    path("produits_noel", views.produits_noel, name="produits_noel"),
    path("produits_horsnoel", views.produits_horsnoel, name="produits_horsnoel"),
]
