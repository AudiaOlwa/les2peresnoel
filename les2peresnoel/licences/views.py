import sweetify
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LicenceRequestForm
from django_htmx.http import HttpResponseClientRedirect
from les2peresnoel.utils import render_block
from django.utils.translation import gettext_lazy as _
from .models import LicenceRequest, Licence
from ..providers.models import Provider
from .forms import LicenceRequestAcceptForm
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.conf import settings
from datetime import timedelta
from django.utils import timezone





@login_required
def licences_request_create(request):
    if request.method == "POST":
        form = LicenceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            licence = form.save(commit=False)
            licence.user = request.user
            licence.save()
            sweetify.toast(request, _("Votre demande de licence a été soumise avec succès."), icon="success")
            return HttpResponseClientRedirect(reverse("licences:list_requests"))
    else:
        form = LicenceRequestForm()
    if request.htmx:
        sweetify.toast(request, _("Votre demande de licence a été soumise avec succès."), icon="error")
        return render_block("licences/requests/create.html", "licences_request_form",  {"form": form})
    return render(request, "licences/requests/create.html", {"form": form})



@login_required
def licences_request_list(request):
    licences = LicenceRequest.objects.all()
    if not request.user.is_superuser or not request.user.is_staff:
        licences = licences.filter(user=request.user)
    return render(request, "licences/requests/list.html", {"requests": licences})

@login_required
def licences_request_details(request, pk):
    licence = LicenceRequest.objects.get(pk=pk)
    form = LicenceRequestAcceptForm()
    return render(request, "licences/requests/details.html", {"licence": licence, "form": form})

@login_required
def licences_request_update(request, pk):
    licence = get_object_or_404(LicenceRequest, pk=pk)
    if request.method == "POST":
        form = LicenceRequestForm(request.POST, request.FILES, instance=licence)
        if form.is_valid():
            licence = form.save(commit=False)
            licence.user = request.user
            licence.save()
            sweetify.toast(request, _("Votre demande de licence a été modifiée avec succès."), icon="success")
            return HttpResponseClientRedirect(reverse("licences:request_list"))
    else:
        form = LicenceRequestForm(instance=licence)
    if request.htmx:
        # sweetify.toast(request, _("Votre demande de licence a été modifiée avec succès."), icon="error")
        return render_block("licences/requests/update.html", "licences_request_form",  {"form": form}) 
    return render(request, "licences/requests/update.html", {"licence": licence, "form": form})

@login_required
def licences_request_delete(request, pk):
    licence = LicenceRequest.objects.get(pk=pk)
    licence.delete()
    sweetify.toast(request, _("Votre demande de licence a été supprimée avec succès."), icon="success")
    return redirect(reverse("licences:list_requests"))


@require_http_methods(["POST"])
@login_required 
@transaction.atomic
def licences_request_accept(request, pk):
    # breakpoint()
    # _form = LicenceRequestAcceptForm(request.POST)
    # if _form.is_valid():
    licence_request = LicenceRequest.objects.get(pk=pk)
    provider, created = Provider.objects.get_or_create(
        account=licence_request.user,
        defaults={
            'licence_key': licence_request.licence_key,
            'company_name': licence_request.company_name,
            'company_address': licence_request.company_address,
            'company_phone': licence_request.company_phone,
            'company_email': licence_request.company_email,
            'company_website': licence_request.company_website,
            'company_logo': licence_request.company_logo,
            'company_country': licence_request.company_country,
            'company_id_number': licence_request.company_id_number,
            'company_description': licence_request.company_description,
        }
    )

    # Générer une licence pour le provider
    licence = Licence.objects.create(
        licence_key=licence_request.licence_key,
        provider=provider,
        owner=licence_request.user,
        is_active=True,
        expires_at=timezone.now() + timedelta(days=settings.LICENCE_EXPIRATION_DAYS),
        created_by=request.user,
        updated_by=request.user, 
    )
    licence_request.accept()
    sweetify.toast(request, _("Votre demande de licence a été acceptée avec succès."), icon="success")
    return redirect(reverse("licences:list_requests"))

@login_required
def licences_request_reject(request, pk):
    licence = LicenceRequest.objects.get(pk=pk)
    licence.reject()
    sweetify.toast(request, _("Votre demande de licence a été rejetée avec succès."), icon="success")
    return redirect(reverse("licences:list_requests"))

@login_required
def licences_list(request):
    licences = Licence.objects.all()
    if not request.user.is_superuser or not request.user.is_staff:
        licences = licences.filter(owner=request.user)
    return render(request, "licences/licences/list.html", {"licences": licences})


@login_required
def licences_licence_create(request):
    if request.method == "POST":
        form = LicenceForm(request.POST, request.FILES)
        if form.is_valid():
            licence = form.save(commit=False)
            licence.user = request.user
            licence.save()
            sweetify.toast(request, _("Votre licence a été créée avec succès."), icon="success")
            return HttpResponseClientRedirect(reverse("licences:licence_list"))
    else:
        form = LicenceForm()
    if request.htmx:
        sweetify.toast(request, _("Votre licence a été créée avec succès."), icon="error")
        return render_block("licences/licence/create.html", "licences_licence_form",  {"form": form})
    return render(request, "licences/licence/create.html", {"form": form})


@login_required
def licences_licence_details(request, pk):
    licence = Licence.objects.get(pk=pk)
    return render(request, "licences/licence/details.html", {"licence": licence})

@login_required
def licences_licence_update(request, pk):
    licence = get_object_or_404(Licence, pk=pk)
    if request.method == "POST":
        licence.update_status()
        sweetify.toast(request, _("Licence mise à jour avec succès."), icon="success")
        return HttpResponseClientRedirect(reverse("licences:list_licences"))
    return render_block("licences/licences/list.html", "update_licence_content",  {"url": licence.get_update_url, "licence": licence})


@login_required
def licences_licence_delete(request, pk):
    licence = get_object_or_404(Licence, pk=pk)
    licence.delete()
    return HttpResponseClientRedirect(reverse("licences:licence_list"))


@login_required
def licences_licence_activate(request, pk):
    licence = get_object_or_404(Licence, pk=pk)
    licence.is_active = True
    licence.save()
    sweetify.toast(request, _("Votre licence a été activée avec succès."), icon="success")
    return HttpResponseClientRedirect(reverse("licences:licence_list"))


@login_required
def licences_licence_deactivate(request, pk):
    licence = get_object_or_404(Licence, pk=pk)
    licence.is_active = False
    licence.save()
    sweetify.toast(request, _("Votre licence a été désactivée avec succès."), icon="success")
    return HttpResponseClientRedirect(reverse("licences:licence_list"))
