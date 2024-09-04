from django.db.models import Model
from django.http import HttpResponse
from django.utils.text import slugify
from render_block import render_block_to_string


def render_block(template_name: str, block_name: str, context: dict) -> HttpResponse:
    return HttpResponse(
        render_block_to_string(
            template_name=template_name, block_name=block_name, context=context
        )
    )


def generate_unique_slug(model_class: Model, text: str, slug_field: str = "slug"):
    """
    Génère un slug unique pour un modèle Django.

    Args :
        model_class : Le modèle Django où vérifier l'unicité du slug.
        text : Le texte à transformer en slug.
        slug_field : Le nom du champ dans le modèle où le slug est stocké. Par défaut, 'slug'.

    Returns :
        Un slug unique sous forme de chaîne de caractères.
    """
    # Transformer le texte en slug
    base_slug = slugify(text)
    slug = base_slug
    counter = 1

    # Vérifier si le slug existe déjà dans la base de données
    while model_class.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
