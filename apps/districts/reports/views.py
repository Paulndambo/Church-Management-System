from django.http import HttpRequest
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render
from django.db.models import F, Sum, DecimalField
import json
from typing import Dict, Any

from collections import OrderedDict


from apps.sections.models import Section
from apps.districts.models import DistrictExpense, KAGDistrictMonthlyReport
from apps.membership.models import Branch

date_today = datetime.now().date()


def district_home(request: HttpRequest):
    district_finance_metrics = get_district_finance_metrics()
    district_attendance_metrics = get_district_attendance_metrics()
    district_expenses_metrics = get_district_expenses_metrics()

    context = {
        "district_finance_metrics": {
            "labels": json.dumps(district_finance_metrics["lablels"]),
            "totals": json.dumps(district_finance_metrics["data"]),
            "expenses": json.dumps(district_expenses_metrics["expenses"]),
        },
        "attendance_metrics": {
            "labels": json.dumps(district_attendance_metrics["labels"]),
            "counts": json.dumps(district_attendance_metrics["counts"]),
        },
        "total_for_year": district_finance_metrics["total_for_year"],
        "total_attendance": district_attendance_metrics["total_attendance"],
        "total_churches": Branch.objects.count(),
        "total_sections": Section.objects.count(),
    }

    return render(request, "districts/home.html", context)


def get_district_finance_metrics(year: int = date_today.year) -> Dict[str, Any]:
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    qs = (
        KAGDistrictMonthlyReport.objects.filter(year=year)
        .annotate(
            total_amount=(
                F("general_fund")
                + F("sunday_school")
                + F("pastors_tithe")
                + F("presbyter_tithe")
                + F("easter")
                + F("special_offering")
                + F("kenya_kids")
                + F("pastors_fund")
                + F("kagdom")
                + F("district_missions")
                + F("resource_mobilisation")
                + F("church_support")
            )
        )
        .values("month")
        .annotate(monthly_total=Sum("total_amount", output_field=DecimalField()))
    )

    # Convert queryset to dict for fast lookup
    qs_dict = {item["month"]: item["monthly_total"] for item in qs}
    # Build ordered dict ensuring all months appear
    monthly_totals = OrderedDict(
        (month, qs_dict.get(month, Decimal("0.00"))) for month in months
    )
    return {
        "lablels": list(monthly_totals.keys()),
        "data": [int(total) for total in monthly_totals.values()],
        "total_for_year": sum(monthly_totals.values()),
    }


def get_district_attendance_metrics(year: int = date_today.year) -> Dict[str, Any]:
    adult_attendance = sum(
        KAGDistrictMonthlyReport.objects.filter(year=year).values_list("adult", flat=True)
    )
    children_attendance = sum(
        KAGDistrictMonthlyReport.objects.filter(year=year).values_list("children", flat=True)
    )

    return {
        "labels": ["Adults", "Children"],
        "counts": [adult_attendance, children_attendance],
        "total_attendance": children_attendance + adult_attendance,
    }


def get_district_expenses_metrics(year: int = date_today.year) -> Dict[str, Any]:
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    qs = (
        DistrictExpense.objects.filter(year=year)
        .values("month")
        .annotate(total_spend=Sum("amount_spend"))
    )

    qs_dict = {item["month"]: item["total_spend"] for item in qs}
    monthly_totals = OrderedDict(
        (month, qs_dict.get(month, Decimal("0.00"))) for month in months
    )

    return {
        "lablels": list(monthly_totals.keys()),
        "expenses": [int(total) for total in monthly_totals.values()],
        "total_for_year": sum(monthly_totals.values()),
    }
