from django.shortcuts import render
from sweetify import sweetify

from .forms import *
from .models import *

# Create your views here.


def products(request):

    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text="Erreur dans la création du produit",
                timer=3000,
            )
    products = Product.objects.all()
    return render(request, "marketplace/products.html", {"products": products})


def categories(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text="Erreur dans la création de la catégorie",
                timer=3000,
            )
    categories = Category.objects.all()
    return render(request, "marketplace/categories.html", {"categories": categories})
