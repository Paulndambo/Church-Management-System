from django.http import HttpRequest
from decimal import Decimal
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from apps.users.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q, Sum
from django.db import transaction

from apps.users.models import User
from apps.sections.models import Section
from apps.districts.models import KAGDistrictMonthlyReport
from apps.core.constants import GENDER_CHOICES, MONTHS_LIST, YEARS_LIST
from apps.districts.models import (
    District,
    DistrictReport,
    DistrictExpense,
)
from apps.membership.models import Branch


# Create your views here.
class DistrictExpenseListView(LoginRequiredMixin, ListView):
    model = DistrictExpense
    template_name = "districts/expenses/expenses.html"
    context_object_name = "expenses"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(month__icontains=search_query)
                | Q(year__icontains=search_query)
                | Q(name__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
@transaction.atomic
def new_expense(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        amount_spend = request.POST.get("amount_spend")
        expense_name = request.POST.get("expense_name")

        report = DistrictReport.objects.get(id=report_id)

        DistrictExpense.objects.create(
            report=report,
            expense_name=expense_name,
            district=report.district,
            month=report.month,
            year=report.year,
            amount_spend=amount_spend,
        )
        return redirect("district-report-details", id=report_id)
    return render(request, "districts/expenses/new_expense.html")


@login_required
def edit_expense(request: HttpRequest):
    if request.method == "POST":
        expense_id = request.POST.get("expense_id")
        amount_spend = request.POST.get("amount_spend")
        expense_name = request.POST.get("expense_name")

        expense = DistrictExpense.objects.get(id=expense_id)
        report = DistrictReport.objects.get(id=expense.report.id)

        DistrictExpense.objects.filter(id=expense_id).update(
            expense_name=expense_name,
            district=report.district,
            month=report.month,
            year=report.year,
            amount_spend=amount_spend,
        )

        return redirect("district-report-details", id=report.id)
    return render(request, "districts/expenses/edit_expense.html")


class PresbytersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "districts/presbyters/presbyters.html"
    context_object_name = "presbyters"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )
        # Get sort parameter
        return queryset.filter(role="Presbyter").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sections"] = Section.objects.filter(presbyter__isnull=True)
        context["districts"] = District.objects.all()
        context["branches"] = Branch.objects.filter(section__has_presbyter=False)
        context["gender_choices"] = GENDER_CHOICES
        return context


@login_required
@transaction.atomic
def new_presbyter(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        id_number = request.POST.get("id_number")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        branch = request.POST.get("branch")
        church_branch = Branch.objects.get(id=branch)
        email = f"{first_name}.{last_name}@gmail.com"

        presbyter = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            id_number=id_number if id_number else phone_number,
            email=email,
            role="Presbyter",
            phone_number=phone_number,
            username=email,
            gender=gender,
            branch=church_branch,
        )
        presbyter.branch.section.presbyter = presbyter
        presbyter.branch.section.has_presbyter = True
        presbyter.branch.section.save()
        return redirect("presbyters")
    return render(request, "districts/presbyters/new_presbyter.html")


@login_required
def edit_presbyter(request: HttpRequest):
    if request.method == "POST":
        presbyter_id = request.POST.get("presbyter_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        id_number = request.POST.get("id_number")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        gender = request.POST.get("gender")
        branch = request.POST.get("branch")

        church_branch = Branch.objects.get(id=branch)

        email = email if email else f"{first_name}.{last_name}@gmail.com"

        user = User.objects.get(id=presbyter_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.id_number = id_number
        user.gender = gender
        user.branch = church_branch
        user.save()

        user.branch.section.presbyter = presbyter
        user.branch.section.has_presbyter = True
        user.branch.section.save()

        return redirect("presbyters")
    return render(request, "districts/presbyters/edit_presbyter.html")


class DistrictReportListView(LoginRequiredMixin, ListView):
    model = DistrictReport
    template_name = "districts/reports.html"
    context_object_name = "reports"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(year__icontains=search_query)
            )

        # Define month order
        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        # Convert queryset to list and sort in Python
        queryset = list(queryset.order_by("year"))  # first sort by year
        queryset.sort(key=lambda x: month_order.index(x.month))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sections"] = Section.objects.all()
        context["districts"] = District.objects.all()
        context["years"] = YEARS_LIST
        context["months"] = MONTHS_LIST
        return context


@login_required
@transaction.atomic
def new_report(request: HttpRequest):
    if request.method == "POST":
        district = request.POST.get("district")
        year = request.POST.get("year")
        month = request.POST.get("month")

        DistrictReport.objects.create(
            district_id=district,
            year=year,
            month=month,
        )
        return redirect("district-reports")
    return render(request, "districts/new_report.html")


@login_required
@transaction.atomic
def edit_report(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        district = request.POST.get("district")
        year = request.POST.get("year")
        month = request.POST.get("month")

        DistrictReport.objects.filter(id=report_id).update(
            district_id=district,
            year=year,
            month=month,
        )
        return redirect("district-reports")
    return render(request, "districts/edit_report.html")


def district_report_details(request: HttpRequest, id: int):
    report = DistrictReport.objects.get(id=id)
    section_reports = get_section_summary(report_id=id)
    

    total_children_attendance = sum(section_reports.values_list("total_children", flat=True))
    total_adult_attendance = sum(section_reports.values_list("total_adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

   
    total_general_fund = sum(section_reports.values_list("total_general_fund", flat=True))
    total_sunday_school = sum(section_reports.values_list("total_sunday_school", flat=True))
    total_pastors_tithe = sum(section_reports.values_list("total_pastors_tithe", flat=True))
    total_pastors_fund = sum(section_reports.values_list("total_pastors_fund", flat=True))
    total_presbyter_tithe = sum(
        section_reports.values_list("total_presbyter_tithe", flat=True)
    )
    total_easter = sum(section_reports.values_list("total_easter", flat=True))
    kenya_kids = sum(section_reports.values_list("total_kenya_kids", flat=True))
    special_offering = sum(section_reports.values_list("total_special_offering", flat=True))

    ten_percent_general_fund = Decimal(0.1) * total_general_fund
    five_percent_sunday_school = Decimal(0.05) * total_sunday_school
    five_percent_pastors_tithe = Decimal(0.05) * total_pastors_tithe
    half_easter_offering = Decimal(0.5) * total_easter

    district_total = (
        ten_percent_general_fund
        + five_percent_sunday_school
        + five_percent_pastors_tithe
        + half_easter_offering
        + kenya_kids
        + special_offering
    )
    district_grand_total = (
        total_general_fund
        + total_sunday_school
        + total_pastors_tithe
        + total_easter
        + kenya_kids
        + special_offering
    )

    sections = Section.objects.all()
    expenses = DistrictExpense.objects.filter(report=report)

    total_expenses = sum(expenses.values_list("amount_spend", flat=True))

    total_kagdom = sum(section_reports.values_list("total_kagdom", flat=True))
    total_resource_mobilisation = sum(
        section_reports.values_list("total_resource_mobilisation", flat=True)
    )
    total_district_missions = sum(
        section_reports.values_list("total_district_missions", flat=True)
    )
    total_church_support = sum(section_reports.values_list("total_church_support", flat=True))
    total_church_welfare = sum(section_reports.values_list("total_church_welfare", flat=True))

    total_additionals = (
        total_kagdom
        + total_resource_mobilisation
        + total_district_missions
        + total_church_support
    )

    context = {
        "report": report,
        "reports": section_reports,
        "total_children_attendance": total_children_attendance,
        "total_adult_attendance": total_adult_attendance,
        "grand_total_attendance": grand_total_attendance,
        "total_sunday_school": total_sunday_school,
        "total_general_fund": total_general_fund,
        "total_pastors_fund": total_pastors_fund,
        "total_pastors_tithe": total_pastors_tithe,
        "total_church_welfare": total_church_welfare,
        "sections": sections,
        "expenses": expenses,
        "five_percent_sunday_school": round(five_percent_sunday_school, 2),
        "ten_percent_general_fund": round(ten_percent_general_fund, 2),
        "five_percent_pastors_tithe": round(five_percent_pastors_tithe, 2),
        "half_easter_offering": round(half_easter_offering, 2),
        "kenya_kids": round(kenya_kids, 2),
        "special_offering": round(special_offering, 2),
        "district_total": round(district_total, 2),
        "total_expenses": total_expenses,
        "district_grand_total": district_grand_total,
        "easter_total": total_easter,
        "total_kagdom": total_kagdom,
        "total_resource_mobilisation": total_resource_mobilisation,
        "total_district_missions": total_district_missions,
        "total_church_support": total_church_support,
        "total_additionals": total_additionals,
        "total_presbyter_tithe": total_presbyter_tithe,
    }
    return render(request, "districts/report_details.html", context)


def district_report(request: HttpRequest, id: int):
    report = DistrictReport.objects.get(id=id)
    #section_reports = KAGDistrictMonthlyReport.objects.filter(report=report)
    section_reports = get_section_summary(report_id=id)

    total_children_attendance = sum(section_reports.values_list("total_children", flat=True))
    total_adult_attendance = sum(section_reports.values_list("total_adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

    
    total_general_fund = sum(section_reports.values_list("total_general_fund", flat=True))
    total_sunday_school = sum(section_reports.values_list("total_sunday_school", flat=True))
    total_pastors_tithe = sum(section_reports.values_list("total_pastors_tithe", flat=True))
    total_pastors_fund = sum(section_reports.values_list("total_pastors_fund", flat=True))
    total_presbyter_tithe = sum(
        section_reports.values_list("total_presbyter_tithe", flat=True)
    )
    total_easter = sum(section_reports.values_list("total_easter", flat=True))
    kenya_kids = sum(section_reports.values_list("total_kenya_kids", flat=True))
    special_offering = sum(section_reports.values_list("total_special_offering", flat=True))

    ten_percent_general_fund = Decimal(0.1) * total_general_fund
    five_percent_sunday_school = Decimal(0.05) * total_sunday_school
    five_percent_pastors_tithe = Decimal(0.05) * total_pastors_tithe
    half_easter_offering = Decimal(0.5) * total_easter

    district_total = (
        ten_percent_general_fund
        + five_percent_sunday_school
        + five_percent_pastors_tithe
        + half_easter_offering
        + kenya_kids
        + special_offering
    )
    district_grand_total = (
        total_general_fund
        + total_sunday_school
        + total_pastors_tithe
        + total_easter
        + kenya_kids
        + special_offering
    )

    sections = Section.objects.all()
    expenses = DistrictExpense.objects.filter(report=report)

    total_expenses = sum(expenses.values_list("amount_spend", flat=True))

    total_kagdom = sum(section_reports.values_list("total_kagdom", flat=True))
    total_resource_mobilisation = sum(
        section_reports.values_list("total_resource_mobilisation", flat=True)
    )
    total_district_missions = sum(
        section_reports.values_list("total_district_missions", flat=True)
    )
    total_church_support = sum(section_reports.values_list("total_church_support", flat=True))
    total_church_welfare = sum(section_reports.values_list("total_church_welfare", flat=True))

    total_additionals = (
        total_kagdom
        + total_resource_mobilisation
        + total_district_missions
        + total_church_support
    )

    first_part = get_section_summary(report_id=id)[:14]#KAGDistrictMonthlyReport.objects.order_by("-created_at").filter(report=report)[:14]
    second_part = get_section_summary(report_id=id)[14:]#KAGDistrictMonthlyReport.objects.order_by("-created_at").filter(report=report)[14:]
    

    context = {
        "report": report,
        "reports": section_reports,
        "first_part": first_part,
        "second_part": second_part,
        "total_children_attendance": total_children_attendance,
        "total_adult_attendance": total_adult_attendance,
        "grand_total_attendance": grand_total_attendance,
        "total_sunday_school": total_sunday_school,
        "total_general_fund": total_general_fund,
        "total_pastors_fund": total_pastors_fund,
        "total_pastors_tithe": total_pastors_tithe,
        "total_church_welfare": total_church_welfare,
        "sections": sections,
        "expenses": expenses,
        "five_percent_sunday_school": round(five_percent_sunday_school, 2),
        "ten_percent_general_fund": round(ten_percent_general_fund, 2),
        "five_percent_pastors_tithe": round(five_percent_pastors_tithe, 2),
        "half_easter_offering": round(half_easter_offering, 2),
        "kenya_kids": round(kenya_kids, 2),
        "special_offering": round(special_offering, 2),
        "district_total": round(district_total, 2),
        "total_expenses": total_expenses,
        "district_grand_total": district_grand_total,
        "easter_total": total_easter,
        "total_kagdom": total_kagdom,
        "total_resource_mobilisation": total_resource_mobilisation,
        "total_district_missions": total_district_missions,
        "total_church_support": total_church_support,
        "total_additionals": total_additionals,
        "total_presbyter_tithe": total_presbyter_tithe,
    }
    return render(request, "districts/district_report.html", context)


@login_required
@transaction.atomic
def delete_section_data(request: HttpRequest):
    if request.method == "POST":
        id = request.POST.get("section_report_id")
        report_id = request.POST.get("report_id")
        section_report = KAGDistrictMonthlyReport.objects.get(id=id)
        section_report.delete()
        return redirect("district-report-details", id=report_id)
    return render(request, "districts/delete_section_data.html")


@login_required
def district_branches(request: HttpRequest):
    branches = Branch.objects.all().order_by("-created_at")
    sections = Section.objects.all()
    context = {"branches": branches, "sections": sections}
    return render(request, "districts/branches/branches.html", context)


@login_required
def new_district_branch(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        town = request.POST.get("town")
        location = request.POST.get("location")
        section = request.POST.get("section")

        branch = Branch.objects.create(
            section_id=section, name=name, location=location, town=town
        )

        return redirect("district-churches")
    return render(request, "districts/branches/new_branch.html")


def get_section_summary(report_id: int):
    return (
        KAGDistrictMonthlyReport.objects
        .filter(report_id=report_id)
        .order_by("-created_at")
        .values("section__id",
            "section__name",
            "report__month",
            "report__year",
            "section__presbyter__first_name",
            "section__presbyter__last_name"
        )
        .annotate(
            total_general_fund=Sum("general_fund"),
            total_sunday_school=Sum("sunday_school"),
            total_pastors_tithe=Sum("pastors_tithe"),
            total_presbyter_tithe=Sum("presbyter_tithe"),
            total_easter=Sum("easter"),
            total_special_offering=Sum("special_offering"),
            total_kenya_kids=Sum("kenya_kids"),
            total_pastors_fund=Sum("pastors_fund"),
            total_kagdom=Sum("kagdom"),
            total_district_missions=Sum("district_missions"),
            total_resource_mobilisation=Sum("resource_mobilisation"),
            total_church_support=Sum("church_support"),
            total_church_welfare=Sum("church_welfare"),
            total_children=Sum("children"),
            total_adult=Sum("adult"),
        )
        .order_by("section__name")
    )