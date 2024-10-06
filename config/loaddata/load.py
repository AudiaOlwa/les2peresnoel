from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

from les2peresnoel.utils import generate_unique_slug


def create_categories_and_subcategories():
    categories_data = {
        "Aliment et boisson": [
            "Chocolat et confiserie",
            "Biscuit et gâteau de Bonheur",
            "Vin et spiritueux",
            "Panettone et autre gâteau traditionnel",
        ],
        "Cadeau et jouet": [
            "Jouet pour enfant",
            "Cadeau personnalisé",
            "Coffret cadeaux",
            "Édition spéciale de livre & Ebook",
            "Édition spéciale de jeu familial",
            "Édition spéciale de jeu vidéo",
        ],
        "Carte de vœu et emballage": [
            "Carte de Bonheur",
            "Papier d'emballage",
            "Ruban et étiquette",
        ],
        "Cosmétique et soin": ["Coffret de beauté", "Parfum", "Produit de soin"],
        "Décoration intérieure et arbre de Bonheur": [
            "Sapin de Bonheur",
            "Filao de Bonheur",
            "Ornement Sapin & Filao",
            "Ornement maison",
            "Pères Bonheur",
            "Personnage Bonheur",
            "Animaux lumineux",
            "Animaux non lumineux",
            "Articles pour animaux",
        ],
        "Décoration extérieure de Bonheur": [
            "Articles de loisirs et de jardinage",
            "Décorations de jardin",
            "Kits de loisirs créatifs",
            "Objet décoratif d'extérieur",
        ],
        "Électronique et technologie": [
            "Gadgets et accessoires technologiques",
            "Jeux vidéo",
            "Produits audio",
        ],
        "Luminaire": [],
        "Vêtement et accessoire": [
            "Tenues Pères Bonheur",
            "Chapeau et écharpe",
            "Tenues Mères Bonheur",
        ],
    }

    for category_name, subcategories in categories_data.items():
        category, _ = Category.objects.get_or_create(name=category_name)
        for subcategory_name in subcategories:
            Category.objects.get_or_create(name=subcategory_name, parent=category)

    print("Catégories et sous-catégories créées avec succès.")


# Appeler la fonction pour créer les catégories et sous-catégories
if __name__ == "__main__":
    create_categories_and_subcategories()
