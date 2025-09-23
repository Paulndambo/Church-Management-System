from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q
from typing import Any
import calendar
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from apps.reports.models import ChurchMonthlyReport
from apps.core.constants import MONTHS_LIST, YEARS_LIST, get_month_number
from apps.membership.models import Branch

# Create your views here.
### Reports Management
class MonthlyReportView(LoginRequiredMixin, ListView):
    model = ChurchMonthlyReport
    template_name = "reports/monthly_reports.html"
    context_object_name = "reports"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(branch__name__icontains=search_query)
                | Q(month_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs: dict[str, Any]):
        context = super().get_context_data(**kwargs)
        context["months"] = MONTHS_LIST
        context["years"] = YEARS_LIST
        context["branches"] = Branch.objects.all()
        return context
    

@login_required
def new_monthly_report(request: HttpRequest):
    if request.method == "POST":
        branch = request.POST.get("branch")
        month_name = request.POST.get("month_name")
        year = request.POST.get("year")
        

        ChurchMonthlyReport.objects.create(
            branch_id=branch,
            month_name=month_name,
            month_number=get_month_number(month_name=month_name),
            year=year
        )

        
        return redirect("monthly-reports")
    return render(request, "reports/new_monthly_report.html")


@login_required
def edit_monthly_report(request: HttpRequest):
    if request.method == "POST":
        branch = request.POST.get("branch")
        report_id = request.POST.get("report_id")
        month_name = request.POST.get("month_name")
        year = request.POST.get("year")
        

        ChurchMonthlyReport.objects.filter(id=report_id).update(
            branch_id=branch,
            month_name=month_name,
            month_number=get_month_number(month_name=month_name),
            year=year
        )

        
        return redirect("monthly-reports")
    return render(request, "reports/edit_monthly_report.html")


@login_required
def monthly_report_details(request: HttpRequest, report_id: int):
    report = ChurchMonthlyReport.objects.get(id=report_id)

    context = {
        'report': report
    }
    return render(request, "reports/monthly_report_details.html", context)