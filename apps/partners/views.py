from typing import Any
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.partners.models import ChurchPartner


# Create your views here.
# Church Projects
class PartnersListView(LoginRequiredMixin, ListView):
    model = ChurchPartner
    template_name = "partners/partners.html"
    context_object_name = "partners"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) | Q(name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs: dict[str, Any]):
        context = super().get_context_data(**kwargs)
        return context


@login_required
@transaction.atomic
def new_partner(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        town = request.POST.get("town")
        country = request.POST.get("country")
        occupation = request.POST.get("occupation")

        ChurchPartner.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            town=town,
            country=country,
            occupation=occupation,
        )

        return redirect("partners")
    return render(request, "partners/new_partner.html")


@login_required
@transaction.atomic
def edit_partner(request: HttpRequest):
    if request.method == "POST":
        partner_id = request.POST.get("partner_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        town = request.POST.get("town")
        country = request.POST.get("country")
        occupation = request.POST.get("occupation")

        ChurchPartner.objects.filter(id=partner_id).update(
            name=name,
            email=email,
            phone_number=phone_number,
            town=town,
            country=country,
            occupation=occupation,
        )

        return redirect("partners")
    return render(request, "partners/edit_partner.html")


@login_required
@transaction.atomic
def delete_partner(request: HttpRequest):
    if request.method == "POST":
        partner_id = request.POST.get("partner_id")
        ChurchPartner.objects.filter(id=partner_id).delete()
        return redirect("partners")
