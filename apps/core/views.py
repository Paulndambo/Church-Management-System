from django.shortcuts import render, redirect
from datetime import datetime
from typing import Any, Dict
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q

import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.http import HttpRequest, HttpResponse

from apps.membership.models import Member
from apps.payments.models import (
    MemberTithing,
    Offering,
    DepartmentSaving,
    ChurchLedger,
    ChurchDonation,
)
from apps.projects.models import ProjectContribution, ProjectPledge, Project
from apps.attendances.models import ServiceAttendanceMetric
from apps.users.models import User

date_today = datetime.now().date()


# Create your views here.
@login_required
def home(request):
    if request.user.role == "District Supritendant":
        return redirect("district-home")
    total_members = Member.objects.count()
    total_department_savings = sum(
        DepartmentSaving.objects.values_list("amount", flat=True)
    )
    tithes_total = sum(MemberTithing.objects.values_list("amount", flat=True))
    total_offerings = sum(Offering.objects.values_list("amount", flat=True))

    projects_pledges = sum(
        ProjectPledge.objects.values_list("amount_pledged", flat=True)
    )
    projects_contributions = sum(
        ProjectContribution.objects.values_list("amount", flat=True)
    )

    attendance_data = get_attendance_yearly_metrics(year=date_today.year)
    service_attendance_data = get_attendance_service_metrics(year=date_today.year)
    monthly_offerings = get_monthly_offerings(year=date_today.year)
    income_expense_data = get_income_expense_data(year=date_today.year)
    monthly_donations = get_monthly_donations(year=date_today.year)
    monthly_tithes = get_monthly_tithes(year=date_today.year)
    monthly_department_savings = get_monthly_department_savings(year=date_today.year)
    monthly_department_savings_metrics = get_monthly_department_savings_metrics(
        year=date_today.year
    )
    gender_distribution = get_gender_distribution()

    total_incomes = sum(income_expense_data["income"])
    total_expenses = sum(income_expense_data["expense"])
    net_balance = total_incomes - total_expenses


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
        "net_financials": {
            "labels": json.dumps(["Total Income", "Total Expenses", "Net Balance"]),
            "data": json.dumps([total_incomes, total_expenses, net_balance]),
        },
        "attendances": {
            "labels": json.dumps(attendance_data["labels"]),
            "counts": json.dumps(attendance_data["attendances"]),
        },
        "monthly_finances": {
            "labels": json.dumps(monthly_offerings["labels"]),
            "offerings": json.dumps(monthly_offerings["offerings"]),
            "donations": json.dumps(monthly_donations["donations"]),
            "tithes": json.dumps(monthly_tithes["tithes"]),
        },
        "income_expense": {
            "labels": json.dumps(income_expense_data["labels"]),
            "income": json.dumps(income_expense_data["income"]),
            "expense": json.dumps(income_expense_data["expense"]),
        },
        "monthly_department_savings": {
            "labels": json.dumps(monthly_department_savings["labels"]),
            "savings": json.dumps(monthly_department_savings["savings"]),
        },
        "monthly_department_savings_metrics": {
            "labels": json.dumps(monthly_department_savings_metrics["labels"]),
            "savings": json.dumps(monthly_department_savings_metrics["savings"]),
        },
        "gender_distribution": {
            "labels": json.dumps(gender_distribution["labels"]),
            "counts": json.dumps(gender_distribution["counts"]),
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
        attendances_data.append(
            {"month": x["month"], "total_attendance": x["total_attendance"]}
        )

    return {
        "labels": [x["month"] for x in yearly_data],
        "attendances": [x["total_attendance"] for x in yearly_data],
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
        services_data.append(
            {"service": x["service__name"], "total_attendance": x["total_attendance"]}
        )

    return {
        "labels": [x["service"] for x in services_data],
        "attendances": [x["total_attendance"] for x in services_data],
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
        offerings_data.append(
            {"month": x["month"], "total_offering": x["total_offering"]}
        )

    return {
        "labels": [x["month"] for x in offerings_data],
        "offerings": [int(x["total_offering"]) for x in offerings_data],
    }


def get_monthly_donations(year: int = date_today.year) -> Dict[str, Any]:
    monthly_data = (
        ChurchDonation.objects.filter(year=year)
        .values("month")
        .annotate(total_donation=Sum("amount"))
        .order_by("donation_date__month")
    )

    donations_data: list[Dict[str, Any]] = []
    for x in monthly_data:
        donations_data.append(
            {"month": x["month"], "total_donation": x["total_donation"]}
        )

    return {
        "labels": [x["month"] for x in donations_data],
        "donations": [int(x["total_donation"]) for x in donations_data],
    }


def get_monthly_tithes(year: int = date_today.year) -> Dict[str, Any]:
    monthly_data = (
        MemberTithing.objects.filter(year=year)
        .values("month")
        .annotate(total_tithe=Sum("amount"))
        .order_by("tithing_date__month")
    )

    tithes_data: list[Dict[str, Any]] = []
    for x in monthly_data:
        tithes_data.append({"month": x["month"], "total_tithe": x["total_tithe"]})

    return {
        "labels": [x["month"] for x in tithes_data],
        "tithes": [int(x["total_tithe"]) for x in tithes_data],
    }


def get_income_expense_data(year: int = date_today.year):
    qs = ChurchLedger.objects.filter(year=year)

    monthly_data = (
        qs.values("month")
        .annotate(
            total_income=Sum("amount", filter=Q(direction="Income")),
            total_expense=Sum("amount", filter=Q(direction="Expense")),
        )
        .order_by("transaction_date__month")
    )

    results: list[Dict[str, Any]] = []

    for entry in monthly_data:
        results.append(
            {
                "month": entry["month"],
                "income": float(entry["total_income"] or 0),
                "expense": float(entry["total_expense"] or 0),
            }
        )

    return {
        "labels": [x["month"] for x in results],
        "income": [x["income"] for x in results],
        "expense": [x["expense"] for x in results],
    }


def get_monthly_department_savings(year: int = date_today.year) -> Dict[str, Any]:
    monthly_data = (
        DepartmentSaving.objects.filter(year=year)
        .values("month")
        .annotate(total_savings=Sum("amount"))
        .order_by("savings_date__month")
    )

    savings_data: list[Dict[str, Any]] = []
    for x in monthly_data:
        savings_data.append({"month": x["month"], "total_savings": x["total_savings"]})

    return {
        "labels": [x["month"] for x in savings_data],
        "savings": [int(x["total_savings"]) for x in savings_data],
    }


def get_monthly_department_savings_metrics(
    year: int = date_today.year,
) -> Dict[str, Any]:
    monthly_data = (
        DepartmentSaving.objects.filter(year=year)
        .values("department__name")
        .annotate(total_savings=Sum("amount"))
        .order_by("department__name")
    )

    savings_data: list[Dict[str, Any]] = []
    for x in monthly_data:
        savings_data.append(
            {"department": x["department__name"], "total_savings": x["total_savings"]}
        )

    return {
        "labels": [x["department"] for x in savings_data],
        "savings": [int(x["total_savings"]) for x in savings_data],
    }


def get_gender_distribution() -> Dict[str, Any]:
    male_count = User.objects.filter(gender="Male").count()
    female_count = User.objects.filter(gender="Female").count()

    return {"labels": ["Male", "Female"], "counts": [male_count, female_count]}
