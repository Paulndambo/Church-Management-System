from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from decimal import Decimal

from apps.payments.models import (
    Offering,
    ChurchLedger,
)
from apps.membership.models import Branch
from apps.attendances.models import ChurchService
from apps.core.models import ChurchOfferingChannel, ChurchOfferingType

from apps.core.constants import format_date, get_month_name

date_today = datetime.now().date()



### Service Offerings
class OfferingsListView(LoginRequiredMixin, ListView):
    model = Offering
    template_name = "offerings/offerings.html"
    context_object_name = "offerings"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(service__name__icontains=search_query)
                | Q(branch__name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all()
        context["services"] = ChurchService.objects.all()
        context["channels"] = ChurchOfferingChannel.objects.all()
        context["offering_types"] = ChurchOfferingType.objects.all()
        return context


@login_required
@transaction.atomic
def new_offering(request: HttpRequest):
    if request.method == "POST":
        branch = request.POST.get("branch")
        service = request.POST.get("service")
        amount = request.POST.get("amount")
        offering_date = request.POST.get("offering_date")
        offering_type = request.POST.get("offering_type")
        offering_channel = request.POST.get("offering_channel")

        date_obj = format_date(offering_date)
        month_name = get_month_name(date_obj.month)
        year = date_obj.year

        offering = Offering.objects.create(
            branch_id=branch,
            service_id=service,
            amount=amount,
            offering_date=offering_date,
            captured_by=request.user,
            month=month_name,
            year=year,
            offering_type_id=offering_type,
            offering_channel_id=offering_channel,
            church=request.user.church,
        )

        ChurchLedger.objects.create(
            name=f"{offering.service.name} {offering_date} Offering",
            description=f"Offering - {offering.service.name} - {offering.branch.name}",
            amount=Decimal(amount),
            direction="Income",
            user=request.user,
            month=month_name,
            year=year,
            transaction_date=offering_date,
            txn_type="Offering",
        )

        return redirect("offerings")
    return render(request, "offerings/new_offering.html")