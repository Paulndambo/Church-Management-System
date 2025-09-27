from django.shortcuts import render, redirect
from datetime import datetime
from typing import Any, Dict
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.http import HttpRequest, HttpResponse

from apps.membership.models import Member
from apps.payments.models import MemberTithing, Offering, DepartmentSaving
from apps.projects.models import ProjectContribution, ProjectPledge, Project
from apps.attendances.models import ServiceAttendanceMetric

date_today = datetime.now().date()
# Create your views here.
@login_required
def home(request):
    if request.user.role == "District Supritendant":
        return redirect("district-reports")
    total_members = Member.objects.count()
    total_department_savings = sum(DepartmentSaving.objects.values_list("amount", flat=True))
    tithes_total = sum(MemberTithing.objects.values_list("amount", flat=True))
    total_offerings = sum(Offering.objects.values_list("amount", flat=True))
    
    projects_pledges = sum(ProjectPledge.objects.values_list("amount_pledged", flat=True))
    projects_contributions = sum(ProjectContribution.objects.values_list("amount", flat=True))

    attendance_data = get_attendance_yearly_metrics(year=date_today.year)
    service_attendance_data = get_attendance_service_metrics(year=date_today.year)
    monthly_offerings = get_monthly_offerings(year=date_today.year)

    print(monthly_offerings)

  
    context = {
        "total_members": total_members,
        "total_department_savings": total_department_savings,
        "tithes_total": tithes_total,
        "total_offerings": total_offerings,
        "projects_pledges": projects_pledges,
        "projects_contributions": projects_contributions,
        "service_attendance": {
            "labels": json.dumps(service_attendance_data["labels"]),
            "attendances": json.dumps(service_attendance_data["attendances"]),
        },
        "monthly_offerings": {
            "labels": json.dumps(monthly_offerings["labels"]),
            "offerings": json.dumps(monthly_offerings["offerings"]),
        },
    }
    return render(request, "home.html", context)


@require_GET
def chart_data_api(request: HttpRequest):
    """API endpoint to get chart data for a specific year"""
    year = request.GET.get("year", datetime.now().year)
    try:
        year = int(year)
    except ValueError:
        year = datetime.now().year

    # Get revenue data for the selected year
    # This is just an example - adjust according to your actual data structure
    attendance_data = get_attendance_yearly_metrics(year=date_today.year)
    service_attendance_data = get_attendance_service_metrics(year=date_today.year)
    monthly_offerings = get_monthly_offerings(year=date_today.year)
    

    return JsonResponse(
        {
            "attendance": attendance_data,
            "service_attendance": service_attendance_data,
            "monthly_offerings": monthly_offerings,
        }
    )


def get_attendance_yearly_metrics(year: int = date_today.year) -> Dict[str, Any]:
    yearly_data = (
        ServiceAttendanceMetric.objects.filter(year=year)
        .values("month")
        .annotate(total_attendance=Sum("total_present"))
        .order_by("service_date__month")
    )

    attendances_data: list[Dict[str, Any]] = []

    for x in yearly_data:
        attendances_data.append({
            "month": x["month"],
            "total_attendance": x["total_attendance"]
        })
   
    return {
        "labels": [x["month"] for x in yearly_data],
        "attendances": [x["total_attendance"] for x in yearly_data]
    }

def get_attendance_service_metrics(year: int = date_today.year) -> Dict[str, Any]:
    service_data = (
        ServiceAttendanceMetric.objects.filter(year=year)
        .values("service__name")
        .annotate(total_attendance=Sum("total_present"))
        .order_by("service__name")
    )

    services_data: list[Dict[str, Any]] = []

    for x in service_data:
        services_data.append({
            "service": x["service__name"],
            "total_attendance": x["total_attendance"]
        })
   
    return {
        "labels": [x["service"] for x in services_data],
        "attendances": [x["total_attendance"] for x in services_data]
    }



def get_monthly_offerings(year: int = date_today.year) -> Dict[str, Any]:
    monthly_data = (
        Offering.objects.filter(year=year)
        .values("month")
        .annotate(total_offering=Sum("amount"))
        .order_by("offering_date__month")
    )

    offerings_data: list[Dict[str, Any]] = []

    for x in monthly_data:
        offerings_data.append({
            "month": x["month"],
            "total_offering": ["total_offering"]
        })
   
    return {
        "labels": [x["month"] for x in monthly_data],
        "offerings": [int(x["total_offering"]) for x in monthly_data]
    }