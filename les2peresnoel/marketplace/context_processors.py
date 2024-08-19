from __future__ import annotations

from django.http import HttpRequest
from .models import Category


def categories(request: HttpRequest) -> dict:
    return {"categories": Category.objects.only('name').all()}
