from django.template.loader import render_to_string
from django.db.transaction import atomic as atomic_transaction
from django_htmx.http import trigger_client_event
import sweetify
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
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
from render_block import render_block_to_string

from ..utils import render_block    
from .forms import *
from .models import *
from .models import Product

from ..core.views import send_order_confirmation_email

SWEETIFY_TOAST_TIMER = settings.SWEETIFY_TOAST_TIMER


# Create your views here.


Cart = get_cart_class()


@require_POST
def add_product(request: HttpRequest, product_id: int, from_cart=False):
    product = get_object_or_404(Product.objects.all(), pk=product_id)
    # breakpoint()
    quantity = int(request.POST.get("quantity", default=1))
    source = request.POST.get("source")
    cart = Cart.new(request)
    if product.is_available_for_quantity(quantity):
        cart.add(product, quantity=quantity)
        sweetify.toast(
            request,
            title="Produit ajouté",
            icon="success",
            text="Produit ajouté avec succès !",
        )
        messages.success(request, message="Produit ajouté avec succès !")
    else:
        sweetify.toast(
            request,
            title="Rupture de stock",
            icon="error",
            text="La quantité de produit souhaitée est indisponible !",
        )
    _context = {"cart": cart}
    if source == "cart":
        response = render_block("layouts/marketplace.html", "cart", _context)
    elif source == "checkout":
        response = render_block("layouts/marketplace.html", "checkout_summary", _context)
    else:
        response = render_block(
            "layouts/marketplace.html", "cart_count", _context
        )

    return trigger_client_event(response=response, name="update_cart", after="receive")


@require_POST
def remove_product(request: HttpRequest):
    # breakpoint()
    item_id = request.POST.get("item_id")
    quantity = int(request.POST.get("quantity", default=1))
    source = request.POST.get("source")
    cart = Cart.new(request)
    _context = {"cart": cart}
    cart.remove(item_id=item_id, quantity=quantity)
    if source and source == "cart":
        return render_block("layouts/marketplace.html", "cart", _context)
    if source and source == "checkout":
        # Todo: Load TVA from settings
        return render_block("layouts/marketplace.html", "checkout_summary", _context)
    return render_block("layouts/marketplace.html", "cart", _context)


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
    product_form = ProductForm(
        request.POST, instance=get_object_or_404(Product, pk=pk))
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
    products = Product.objects.only('pk', 'name', 'category', 'price', 'image')

    max_price = max([product.price for product in products])

    min_price = min([product.price for product in products])

    filter_categories_slugs = []
    if request.htmx:
        # breakpoint()
        for item in request.GET:
            if item.startswith('filter_category_'):
                filter_categories_slugs.append(request.GET.get(item))
        if filter_categories_slugs != []:
            products = products.filter(
                category__slug__in=filter_categories_slugs)

        filter_price_from = int(request.GET.get('filter_price_from') or 0)
        filter_price_to = int(request.GET.get('filter_price_to') or 0)
        if filter_price_from != 0 and filter_price_to != 0 and filter_price_from < filter_price_to:
            products = products.filter(
                price__gte=filter_price_from, price__lte=filter_price_to)
    paginator = Paginator(products, 9)
    page = request.GET.get("page")
    form = ProductForm()
    products = paginator.get_page(page)
    _context = {
        "categories": Category.objects.only('name', 'cover_image'),
        "products": products,
        "filter_datas": {
            "min_price": int(min_price),
            "start_min_price": 10,
            "max_price": int(max_price),
            "start_max_price": 90,
            "filter_categorie_slug": filter_categories_slugs
        }
    }
    if request.htmx:
        return render_block("marketplace/home.html", "product_list", _context)
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


def checkout(request):
    cart = Cart.new(request)
    # Shipping form
    checkout_form = CheckoutForm()
    cart_tva_amount = 1.18*float(cart.total)
    shipping_fees = settings.SHIPPING_FEES
    total_amount = cart_tva_amount + shipping_fees
    _context = {
        "checkout_form": checkout_form,
        "shipping_fees": shipping_fees,
        "total_amount": total_amount,
        "cart_tva_amount": cart_tva_amount
    }
    return render(request, "marketplace/checkout.html", _context)

class CheckoutView(View):
    def get(self, request, *args, **kwars):
        cart = Cart.new(request)
        # Shipping form
        checkout_form = CheckoutForm()
        cart_tva_amount = 1.18*float(cart.total)
        shipping_fees = settings.SHIPPING_FEES
        total_amount = cart_tva_amount + shipping_fees
        _context = {
            "checkout_form": checkout_form,
            "total_amount": total_amount,
            "cart_tva_amount": cart_tva_amount
        }
        return render(request, "marketplace/checkout.html", _context)
    
    def post(self, request, *args, **kwargs):
        # breakpoint()
        checkout_form = CheckoutForm(request.POST)
        cart = Cart.new(request)
        tva_amount = 0.18*float(cart.total)
        cart_tva_amount = 1.18*float(cart.total)
        # shipping_fees = settings.SHIPPING_FEES
        total_amount = cart_tva_amount
        customer = request.user if request.user.is_authenticated else None
        if checkout_form.is_valid():
            with atomic_transaction():
                checkout = checkout_form.save()
                order = Order.objects.create(**{
                    "last_name": checkout.last_name,
                    "first_name": checkout.first_name,
                    "email": checkout.email,
                    "total_ht": cart.total,
                    "total_ttc": total_amount,
                    "total_tva": tva_amount,
                    "checkout": checkout,
                    "customer": customer
                })

                OrderItem.objects.bulk_create(
                    [
                        OrderItem(**{
                            "product": item.product,
                            "order": order,
                            "quantity": item.quantity,
                            "price": item.price,
                            "total": item.subtotal
                        })
                        for item in cart
                    ]
                )
                cart.empty()
                sweetify.toast(request, _("Votre commande a été enregistrée avec succès !"))
            if order:
                # if not order.tracking_number:
                #     order.tracking_number = order.generate_tracking_number
                send_order_confirmation_email(order)
            return redirect(order.get_payment_url)
        else:
            sweetify.toast(request, _("Une erreur s'est produite !"), "error")
        return self.get(request, *args, **kwargs)
                    

            
        

@require_POST
def update_checkout(request):
    cart = Cart.new(request)
    cart_tva_amount = 1.18*float(cart.total)
    shipping_fees = shipping_fees
    total_amount = cart_tva_amount + shipping_fees
    _context = {
        "cart": cart,
        "cart_tva_amount": cart_tva_amount,
        "shipping_fees": settings.SHIPPING_FEES,
        "total_amount": total_amount,
    }
    return render_block("marketplace/checkout.html", "checkout", _context)