from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LicenceRequestForm
from django_htmx.http import HttpResponseClientRedirect
from les2peresnoel.utils import render_block



@login_required
def request_licence(request):
    if request.method == "POST":
        form = LicenceRequestForm(request.POST)
        if form.is_valid():
            licence = form.save(commit=False)
            licence.user = request.user
            licence.save()
            return HttpResponseClientRedirect("licences:request_licence")
    else:
        form = LicenceRequestForm()
    if request.htmx:
        return render_block("licences/request.html", "licences_request_form",  {"form": form})
    return render(request, "licences/request.html", {"form": form})