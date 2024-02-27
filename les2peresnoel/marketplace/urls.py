from django.urls import path, re_path

from . import views

app_name = "marketplace"

urlpatterns = [path("/", views.products, name="")]
