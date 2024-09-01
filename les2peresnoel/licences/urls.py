from django.urls import path

from . import views

app_name = "licences"

urlpatterns = [
    path("request", views.request_licence, name="request")
]