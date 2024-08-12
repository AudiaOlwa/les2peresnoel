from dj_shop_cart.cart import get_cart_class
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRedirect
from sweetify import sweetify

from ..utils import render_block
from .forms import *
from .models import *
from .models import Product

SWEETIFY_TOAST_TIMER = settings.SWEETIFY_TOAST_TIMER


# Create your views here.


Cart = get_cart_class()


@require_POST
def add_product(request: HttpRequest, product_id: int, from_cart=False):
    product = get_object_or_404(Product.objects.all(), pk=product_id)
    # breakpoint()
    quantity = int(request.POST.get("quantity", default=1))
    cart = Cart.new(request)
    cart.add(product, quantity=quantity)
    sweetify.toast(
        request,
        title="Produit ajouté",
        icon="success",
        text="Produit ajouté avec succès !",
    )
    messages.success(request, message="Produit ajouté avec succès !")
    from_cart = eval(from_cart)
    if from_cart:
        return render_block("layouts/marketplace.html", "cart", context={"cart": cart})
    return render_block(
        "layouts/marketplace.html", "cart_count", context={"cart": cart}
    )


@require_POST
def remove_product(request: HttpRequest):
    breakpoint()
    item_id = request.POST.get("item_id")
    quantity = int(request.POST.get("quantity", default=1))
    cart = Cart.new(request)
    cart.remove(item_id=item_id, quantity=quantity)
    return render_block("layouts/marketplace.html", "cart", context={"cart": cart})


@require_POST
def empty_cart(request: HttpRequest):
    Cart.new(request).empty()
    ...


def list_category(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la création de la catégorie"),
                timer=SWEETIFY_TOAST_TIMER,
            )
    categories = Category.objects.all()
    return render(
        request, "marketplace/categories/list.html", {"categories": categories}
    )


def create_category(request):
    category_form = CategoryForm(request.POST)
    if request.method == "POST":
        if category_form.is_valid():
            category_form.save()
            sweetify.toast(
                request=request,
                title=_("Catégorie créée"),
                icon="success",
                text=_("La catégorie a bien été crée"),
                timer=SWEETIFY_TOAST_TIMER,
            )
            return redirect("marketplace:create_category")
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la création de la catégorie"),
                timer=SWEETIFY_TOAST_TIMER,
            )
    return render(
        request, "marketplace/categories/create.html", context={"form": category_form}
    )


def detail_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(
        request, "marketplace/categories/detail.html", context={"category": category}
    )


def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category_form = CategoryForm(request.POST, instance=category)
    if request.method == "POST":
        if category_form.is_valid():
            category_form.save()
            sweetify.toast(
                request=request,
                title=_("Catégorie mise à jour"),
                icon="success",
                text=_("La catégorie a bien été mise à jour"),
                timer=SWEETIFY_TOAST_TIMER,
            )
            return redirect("marketplace:detail_category")
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la création de la catégorie"),
                timer=SWEETIFY_TOAST_TIMER,
            )
    return render(
        request, "marketplace/categories/update.html", context={"form": category_form}
    )


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("marketplace:categories")
    return render(
        request, "marketplace/categories/delete.html", context={"category": category}
    )


def list_product(request):
    products = Product.objects.filter(user=request.user)
    # paginate by 20
    paginator = Paginator(products, 20)
    page = request.GET.get("page")
    products = paginator.get_page(page)
    return render(request, "marketplace/products/list.html", {"products": products})


def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_images = ProductImage.objects.filter(product=product)
    return render(
        request,
        "marketplace/products/detail.html",
        context={"product": product, "product_images": product_images},
    )


def create_product(request):
    product_form = ProductForm(request.POST)
    if request.method == "POST":
        if product_form.is_valid():
            product_form.save()
            return redirect("marketplace:create_product")
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la création du produit"),
                timer=SWEETIFY_TOAST_TIMER,
            )
    return render(
        request, "marketplace/products/create.html", context={"form": product_form}
    )


def update_product(request, pk):
    product_form = ProductForm(request.POST, instance=get_object_or_404(Product, pk=pk))
    if request.method == "POST":
        if product_form.is_valid():
            product_form.save()
            sweetify.toast(
                request=request,
                title=_("Produit mis à jour"),
                icon="success",
                text=_("Le produit a bien été mis à jour"),
                timer=SWEETIFY_TOAST_TIMER,
            )
            return redirect("marketplace:detail_product", pk=pk)
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la mise à jour du produit"),
                timer=SWEETIFY_TOAST_TIMER,
            )
    return render(
        request, "marketplace/products/update.html", context={"form": product_form}
    )


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("marketplace:products")
    return render(
        request, "marketplace/products/delete.html", context={"product": product}
    )


def add_image_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_image_form = ProductImageForm(request.POST, request.FILES)
    if request.method == "POST":
        if product_image_form.is_valid():
            product_image_form.save()
            sweetify.toast(
                request=request,
                title=_("Image ajoutée"),
                icon="success",
                text=_("L'image a bien été ajoutée"),
                timer=SWEETIFY_TOAST_TIMER,
            )
            return redirect("marketplace:detail_product", pk=pk)
        else:
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la création de l'image"),
                timer=SWEETIFY_TOAST_TIMER,
            )
    return render(
        request,
        "marketplace/products/add_image.html",
        context={"form": product_image_form},
    )


def home(request):
    _context = {
        "categories": Category.objects.all(),
        "products": Product.objects.all(),
    }
    return render(request, "marketplace/home.html", context=_context)


def dashboard(request):
    return render(request, "marketplace/admin/index.html")


def update_cart_count(request):
    cart = Cart.new(request)
    return render_block(
        "layouts/marketplace.html", "cart_details_count", {"cart": cart}
    )


def update_cart(request):
    cart = Cart.new(request)
    return render_block("layouts/marketplace.html", "cart", {"cart": cart})
