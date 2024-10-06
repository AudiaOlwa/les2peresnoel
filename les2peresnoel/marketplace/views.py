import sweetify
from dj_shop_cart.cart import get_cart_class
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.transaction import atomic as atomic_transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.http import require_POST
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from render_block import render_block_to_string

from ..core.views import send_order_confirmation_email
from ..utils import render_block
from .forms import *
from .models import *
from .models import Product

SWEETIFY_TOAST_TIMER = settings.SWEETIFY_TOAST_TIMER


# Create your views here.


Cart = get_cart_class()


def home(request):
    products = (
        Product.get_available()
    )  # .only('pk', 'name', 'category', 'price', 'image')
    try:
        max_price = max([product.price for product in products])
    except:
        max_price = 0
    try:
        min_price = min([product.price for product in products])
    except:
        min_price = 0

    products = (
        products.filter(category__slug__icontains="bonheur")
        .exclude(media="")
        .distinct()
    )
    filter_categories_slugs = []
    if request.htmx:
        # breakpoint()
        for item in request.GET:
            if item.startswith("filter_category_"):
                filter_categories_slugs.append(request.GET.get(item))
        if filter_categories_slugs != []:
            products = products.filter(category__slug__in=filter_categories_slugs)

        filter_price_from = int(request.GET.get("filter_price_from") or 0)
        filter_price_to = int(request.GET.get("filter_price_to") or 0)
        if (
            filter_price_from != 0
            and filter_price_to != 0
            and filter_price_from < filter_price_to
        ):
            products = products.filter(
                price__gte=filter_price_from, price__lte=filter_price_to
            )
    paginator = Paginator(products, 9)
    page = request.GET.get("page")
    form = ProductForm()
    products = paginator.get_page(page)
    _context = {
        "categories": Category.objects.only("name", "cover_image", "slug").filter(
            slug__icontains="bonheur"
        ),
        "all_categories": Category.objects.only("name", "cover_image", "slug").filter(
            parent__isnull=True
        ),
        "products": products,
        "filter_datas": {
            "min_price": int(min_price),
            "start_min_price": 10,
            "max_price": int(max_price),
            "start_max_price": 90,
            "filter_categorie_slug": filter_categories_slugs,
        },
    }
    if request.htmx:
        return render_block("marketplace/home.html", "product_list", _context)
    return render(request, "marketplace/home.html", context=_context)


@require_POST
def add_product(request: HttpRequest, product_id: int, from_cart=False):
    product = get_object_or_404(Product.objects.all(), pk=product_id)
    # breakpoint()
    quantity = int(request.POST.get("quantity", default=1))
    source = request.POST.get("source")
    cart = Cart.new(request)
    # get the provider of the first product in cart
    # breakpoint()
    if cart.count > 0:
        first_product = cart.products[0]
        existing_provider = first_product.owner
    else:
        existing_provider, first_product = None, None

    if not first_product or (
        (not first_product.media or not product.media)
        and (first_product.media or product.media)
    ):
        sweetify.warning(
            request,
            title=_("Information"),
            text=_(
                "Vous ne pouvez pas mélanger les produits numériques et physiques dans le même panier \n"
            ),
            button=_("Compris !"),
            persistent=True,
            icon="info",
        )
        return HttpResponseClientRedirect(reverse("marketplace:home"))
    if existing_provider and existing_provider != product.owner:
        sweetify.warning(
            request,
            # title=_("Erreur !"),
            title=_("Information"),
            icon="info",
            text=_(
                "Vous ne pouvez pas ajouter des produits de différents fournisseurs dans le même panier \n"
                # "Terminer votre commande ou vider votre panier"
            ),
            button=_("Compris !"),
            # timer=SWEETIFY_TOAST_TIMER,
            persistent=True,
        )
        return HttpResponseClientRedirect(reverse("marketplace:home"))
    # else:
    #     provider = product.owner

    cart.add(product, quantity=quantity)
    sweetify.toast(
        request,
        title="Produit ajouté",
        icon="success",
        text="Produit ajouté avec succès !",
    )
    messages.success(request, message="Produit ajouté avec succès !")
    _context = {"cart": cart}
    if source == "cart":
        response = render_block("layouts/marketplace.html", "cart", _context)
    elif source == "checkout":
        response = render_block(
            "layouts/marketplace.html", "checkout_summary", _context
        )
    else:
        response = render_block("layouts/marketplace.html", "cart_count", _context)
        # response = TemplateResponse(request, "layouts/marketplace.html", _context)

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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("marketplace:products")
    return render(
        request, "marketplace/products/delete.html", context={"product": product}
    )


@login_required
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
    cart_tva_amount = 1.18 * float(cart.total)
    shipping_fees = settings.SHIPPING_FEES
    total_amount = cart_tva_amount + shipping_fees
    _context = {
        "checkout_form": checkout_form,
        "shipping_fees": shipping_fees,
        "total_amount": total_amount,
        "cart_tva_amount": cart_tva_amount,
    }
    return render(request, "marketplace/checkout.html", _context)


class CheckoutView(LoginRequiredMixin, View):
    login_url = "/login/"  # Remplacez par l'URL de votre page de connexion

    def get(self, request, *args, **kwars):
        cart = Cart.new(request)
        # Shipping form
        tva = settings.TVA_RATE / 100
        checkout_form = CheckoutForm()
        cart_tva_amount = 1.055 * float(cart.total)
        shipping_fees = settings.SHIPPING_FEES
        total_amount = cart_tva_amount + shipping_fees
        _context = {
            "checkout_form": checkout_form,
            "total_amount": total_amount,
            "cart_tva_amount": cart_tva_amount,
        }
        return render(request, "marketplace/checkout.html", _context)

    def post(self, request, *args, **kwargs):
        # breakpoint()
        tva = settings.TVA_RATE / 100
        checkout_form = CheckoutForm(request.POST)
        cart = Cart.new(request)
        tva_amount = float(tva) * float(cart.total)
        cart_tva_amount = float(1 + tva) * float(cart.total)
        # shipping_fees = settings.SHIPPING_FEES
        total_amount = cart_tva_amount
        customer = request.user if request.user.is_authenticated else None
        if checkout_form.is_valid():
            with atomic_transaction():
                checkout = checkout_form.save()
                order = Order.objects.create(
                    **{
                        "last_name": checkout.last_name,
                        "first_name": checkout.first_name,
                        "email": checkout.email,
                        "total_ht": cart.total,
                        "total_ttc": total_amount,
                        "total_tva": tva_amount,
                        "checkout": checkout,
                        "customer": customer,
                    }
                )

                OrderItem.objects.bulk_create(
                    [
                        OrderItem(
                            **{
                                "product": item.product,
                                "order": order,
                                "quantity": item.quantity,
                                "price": item.price,
                                "total": item.subtotal,
                            }
                        )
                        for item in cart
                    ]
                )
                cart.empty()
                sweetify.toast(
                    request, _("Votre commande a été enregistrée avec succès !")
                )
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
    cart_tva_amount = 1.18 * float(cart.total)
    shipping_fees = shipping_fees
    total_amount = cart_tva_amount + shipping_fees
    _context = {
        "cart": cart,
        "cart_tva_amount": cart_tva_amount,
        "shipping_fees": settings.SHIPPING_FEES,
        "total_amount": total_amount,
    }
    return render_block("marketplace/checkout.html", "checkout", _context)


@login_required
def order_list(request):
    orders = Order.objects.all()
    if not request.user.is_superuser:
        orders = orders.filter(customer=request.user)
    return render(request, "marketplace/orders/list.html", {"orders": orders})


@login_required
def order_details(request, pk):
    # if not request.user.is_provider and not request.user.is_superuser:
    #     raise HttpResponseUnauthorized(
    #         _("Vous n'êtes pas autorisé à accéder à cette page")
    #     )
    order = get_object_or_404(Order, pk=pk)
    return render_block(
        "marketplace/orders/list.html", "order_detail_content", {"order": order}
    )


def order_tracking(request, tracking_id):
    order = get_object_or_404(Order, tracking_number=tracking_id)
    return render(request, "marketplace/orders/tracking.html", {"order": order})


def list_product_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    _categories = Category.objects.all()
    return render(
        request,
        "marketplace/products/list.html",
        {"products": products, "category": category, "categories": _categories},
    )


def simple_checkout(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Calculer les montants pour un seul produit
    tva = settings.TVA_RATE / 100
    price_tva_amount = (1 + tva) * float(product.price)
    shipping_fees = settings.SHIPPING_FEES
    total_amount = price_tva_amount + shipping_fees

    # Créer un formulaire de commande pré-rempli
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }
    checkout_form = CheckoutForm(initial=initial_data)

    context = {
        "product": product,
        "checkout_form": checkout_form,
        "price_tva_amount": price_tva_amount,
        "shipping_fees": shipping_fees,
        "total_amount": total_amount,
    }

    if request.method == "POST":
        tva = settings.TVA_RATE / 100
        checkout_form = CheckoutForm(request.POST)
        tva_amount = float(tva) * product.price
        cart_tva_amount = float(1 + tva) * float(product.price)
        # shipping_fees = settings.SHIPPING_FEES
        total_amount = cart_tva_amount
        customer = request.user if request.user.is_authenticated else None
        if checkout_form.is_valid():
            with atomic_transaction():
                checkout = checkout_form.save()
                order = Order.objects.create(
                    **{
                        "last_name": checkout.last_name,
                        "first_name": checkout.first_name,
                        "email": checkout.email,
                        "total_ht": cart.total,
                        "total_ttc": total_amount,
                        "total_tva": tva_amount,
                        "checkout": checkout,
                        "customer": customer,
                    }
                )

                OrderItem.objects.bulk_create(
                    [
                        OrderItem(
                            **{
                                "product": product,
                                "order": order,
                                "quantity": 1,
                                "price": product.price,
                                "total": product.price,
                            }
                        )
                        for item in cart
                    ]
                )
                sweetify.toast(
                    request, _("Votre commande a été enregistrée avec succès !")
                )
            if order:
                # if not order.tracking_number:
                #     order.tracking_number = order.generate_tracking_number
                send_order_confirmation_email(order)
            return redirect(order.get_payment_url)
        else:
            sweetify.toast(request, _("Une erreur s'est produite !"), "error")
    return render(request, "marketplace/simple_checkout.html", context)
    # return redirect("marketplace:checkout")
