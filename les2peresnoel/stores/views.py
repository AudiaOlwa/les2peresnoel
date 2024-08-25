import sweetify
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseClientRedirect

from config.settings import SWEETIFY_TOAST_TIMER
from les2peresnoel.marketplace.forms import ProductForm, ProductAddForm
from les2peresnoel.marketplace.models import Product
from les2peresnoel.utils import render_block

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views import View

class SweetifyMixin:
    def notify_success(self, request, message):
        sweetify.toast(
            request=request,
            title="Succès",
            icon="success",
            text=message,
            timer=SWEETIFY_TOAST_TIMER,
        )

    def notify_error(self, request, message):
        sweetify.toast(
            request=request,
            title="Erreur",
            icon="error",
            text=message,
            timer=SWEETIFY_TOAST_TIMER,
        )

@login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user)
    # paginate by 20
    paginator = Paginator(products, 20)
    page = request.GET.get("page")
    form = ProductForm()
    products = paginator.get_page(page)
    return render(
        request, "stores/products/list.html", {
            "products": products, "form": form}
    )


@login_required
def product_create(request):
    product_form = ProductForm()
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        try:
            if product_form.is_valid():
                product_form.instance.owner = request.user
                product_form.save()
                if request.htmx:
                    return HttpResponseClientRedirect(reverse("stores:product_list"))
            else:
                sweetify.toast(
                    request=request,
                    title="Erreur",
                    icon="error",
                    text=_("Erreur dans la création du produit"),
                    timer=SWEETIFY_TOAST_TIMER,
                )
        except Exception as e:
            # Todo :: Log the error with thw date it's occured
            sweetify.toast(
                request=request,
                title="Erreur",
                icon="error",
                text=_("Erreur dans la création du produit"),
                timer=SWEETIFY_TOAST_TIMER,
            )
            raise e
    return render_block(
        "stores/products/list.html",
        "form_product_content",
        context={"form": product_form},
    )
    # return render(
    #     request, "stores/products/create.html", context={"form": product_form}
    # )


@login_required
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # product_images = ProductImage.objects.filter(product=product)
    return render(
        request,
        "stores/products/detail.html",
        context={"product": product},
    )


@login_required
def product_update(request, pk):
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
        request, "stores/products/update.html", context={"form": product_form}
    )


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("stores:products")
    return render(request, "stores/products/delete.html", context={"product": product})


class OnProductAddView(SweetifyMixin, View):
    template_name = 'stores/products/partials/add.html'
    
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        form = ProductAddForm()
        return render(request, self.template_name, {'form': form, 'product': product})

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        form = ProductAddForm(request.POST)
        
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            product.quantity += quantity  # Ajoute la quantité au produit existant
            product.save()
            self.notify_success(request, "Quantité ajoutée avec succès.")
            return HttpResponseClientRedirect(reverse('stores:product_list'))
        
        self.notify_error(request, "Erreur lors de l'ajout de la quantité.")
        return self.render_to_response({'form': form, 'product': product})


class OnProductEditView(SweetifyMixin, UpdateView):
    model = Product
    template_name = 'stores/products/partials/edit.html'
    form_class = ProductForm
    success_url = reverse_lazy('stores:product_list')

    def form_valid(self, form):
        form.save()
        self.notify_success(self.request, "Produit mis à jour avec succès.")
        return HttpResponseClientRedirect(self.success_url)

    def form_invalid(self, form):
        self.notify_error(self.request, "Erreur lors de la mise à jour du produit.")
        return self.render_to_response({'form': form})


class OnProductDeleteView(SweetifyMixin, DeleteView):
    model = Product
    template_name = 'stores/products/partials/delete.html'
    success_url = reverse_lazy('stores:product_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        self.notify_success(self.request, "Produit supprimé avec succès.")
        return HttpResponseClientRedirect(self.success_url)


class OnProductDetailsView(DetailView):
    model = Product
    template_name = 'stores/products/partials/details.html'