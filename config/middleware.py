from threading import local

from django.conf import settings
from django.shortcuts import redirect

_thread_data = local()


class CurrentRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_data.request = request
        response = self.get_response(request)
        return response


class RedirectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_complete = request.build_absolute_uri()
        if any(domain in url_complete for domain in settings.MARKETPLACE_DOMAINS):
            return redirect("marketplace:home")
        return self.get_response(request)
