import random

from django.shortcuts import get_object_or_404, render
from django.utils.translation import activate
from django.utils.translation import gettext as _

from .forms import SignUpForm
from .models import Document, Product


# Create your views here.
def signup(request):
    message = _("Hello, world!")
    activate("fr")
    form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def index(request):
    message = _("Hello, world!")
    activate("fr")
    product_book_all = Product.objects.filter(type="L")
    random_books = random.sample(list(product_book_all), 3)

    product_video_all = Product.objects.filter(type="V")
    random_video = random.sample(list(product_video_all), 1)

    product_musik_all = Product.objects.filter(type="M")
    random_musik = random.sample(list(product_musik_all), 2)

    return render(
        request,
        "index.html",
        {
            "random_books": random_books,
            "random_video": random_video,
            "random_musik": random_musik,
        },
    )


def about(request):
    message = _("Hello, world!")
    activate("fr")
    return render(request, "about.html")


def gallerie(request):
    message = _("Hello, world!")
    activate("fr")
    return render(request, "gallerie.html")


def evolution(request):
    message = _("Hello, world!")
    activate("fr")
    return render(request, "evolution.html")


def prqw2pn(request):
    message = _("Hello, world!")
    activate("fr")
    return render(request, "prqw2pn.html")


def produits_noel(request):
    message = _("Hello, world!")
    activate("fr")
    return render(request, "produits_noel.html")


def produits_horsnoel(request):
    message = _("Hello, world!")
    activate("fr")
    return render(request, "produits_horsnoel.html")


def birth(request):
    message = _("Hello, world!")
    activate("fr")
    birth = Document.objects.all()
    return render(request, "birth.html", {"birth": birth})


def boutique(request):
    message = _("Hello, world!")
    activate("fr")
    product_book_all = Product.objects.filter(type="L")
    random_books = random.sample(list(product_book_all), 3)
    product_video_all = Product.objects.filter(type="V")
    random_video = random.sample(list(product_video_all), 3)
    product_musik_all = Product.objects.filter(type="M")
    random_musik = random.sample(list(product_musik_all), 3)
    return render(
        request,
        "boutique.html",
        {
            "random_books": random_books,
            "random_video": random_video,
            "random_musik": random_musik,
        },
    )


# def livre(request):
# 	product_book_all = Product.objects.filter(type='L')
# 	random_books = random.sample(list(product_book_all), len(product_book_all))
# 	return render(request, 'livre.html',{'random_books': random_books})


def livre(request, livre_id):
    message = _("Hello, world!")
    activate("fr")
    # Récupérer le livre spécifique en fonction de l'identifiant
    livre = get_object_or_404(Product, id=livre_id)
    # Récupérer tous les livres (similaire à la logique de product_book_all dans la vue livre)
    product_book_all = Product.objects.filter(type="L")
    random_books = random.sample(list(product_book_all), len(product_book_all))
    # Passer le livre spécifique et les livres aléatoires à la vue
    return render(request, "livre.html", {"livre": livre, "random_books": random_books})


# def musique(request):
# 	product_musik_all = Product.objects.filter(type='M')
# 	random_musik = random.sample(list(product_musik_all), len(product_musik_all))
# 	return render(request, 'musique.html',{'random_musik': random_musik})
def musique(request, musik_id):
    message = _("Hello, world!")
    activate("fr")

    # Récupérer la musique spécifique en fonction de l'identifiant
    musik = get_object_or_404(Product, id=musik_id)

    # Récupérer toutes les musiques (similaire à la logique de product_musik_all dans la vue musique)
    product_musik_all = Product.objects.filter(type="M")
    random_musik = random.sample(list(product_musik_all), len(product_musik_all))

    # Passer la musique spécifique et les musiques aléatoires à la vue
    return render(
        request, "musique.html", {"musik": musik, "random_musik": random_musik}
    )


# def video(request):
# 	product_video_all = Product.objects.filter(type='V')
# 	random_video = random.sample(list(product_video_all), len(product_video_all))
# 	return render(request, 'video.html',{'random_video': random_video})
def video(request, video_id):
    message = _("Hello, world!")
    activate("fr")

    # Récupérer la vidéo spécifique en fonction de l'identifiant
    video = get_object_or_404(Product, id=video_id)

    # Récupérer toutes les vidéos
    product_video_all = Product.objects.filter(type="V")

    # Mélanger les vidéos (si nécessaire)
    random_video = random.sample(list(product_video_all), len(product_video_all))

    # Passer la vidéo spécifique et les vidéos aléatoires à la vue
    return render(request, "video.html", {"video": video, "random_video": random_video})
