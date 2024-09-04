from django.urls import path

from . import views

app_name = "licences"

urlpatterns = [
    path(
        "request", 
        views.licences_request_create, 
        name="request_create"
    ),
    path(
        "request/list", 
        views.licences_request_list, 
        name="list_requests"
    ),
    
    path(
        "request/<uuid:pk>/",
        views.licences_request_details,
        name="request_details"
    ),
    path(
        "request/<uuid:pk>/update",
        views.licences_request_update,
        name="request_update"
    ),
    path(
        "request/<uuid:pk>/accept",
        views.licences_request_accept,
        name="request_accept"
    ),
    path(
        "request/<uuid:pk>/reject",
        views.licences_request_reject,
        name="request_reject"
    ),
    path(
        "request/<uuid:pk>/delete",
        views.licences_request_delete,
        name="request_delete"
    ),
    path(
        "licence/list", 
        views.licences_list, 
        name="list_licences"
    ),
    path(
        "licence/create",
        views.licences_licence_create,
        name="licence_create"
    ),
    path(
        "licence/<uuid:pk>/",
        views.licences_licence_details,
        name="licence_details"
    ),
    path(
        "licence/<uuid:pk>/update",
        views.licences_licence_update,
        name="licence_update"
    ),
    path(
        "licence/<uuid:pk>/delete",
        views.licences_licence_delete,
        name="licence_delete"
    ),
]