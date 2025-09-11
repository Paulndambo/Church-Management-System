from django.http import HttpRequest
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.users.models import User, Visitor
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.db import transaction

from apps.users.models import User
from apps.sections.models import Section
from apps.core.constants import GENDER_CHOICES, MONTHS_LIST, YEARS_LIST
from apps.districts.models import District, DistrictAttendance, DistrictFinance, DistrictReport, DistrictExpense

# Create your views here.
def district_home(request: HttpRequest):
    return render(request, "districts/home.html")


class DistrictAttendanceListView(LoginRequiredMixin, ListView):
    model = DistrictAttendance
    template_name = "districts/attendances.html"
    context_object_name = "attendances"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(month__icontains=search_query)
                | Q(year__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class DistrictFinanceListView(LoginRequiredMixin, ListView):
    model = DistrictFinance
    template_name = "districts/finances.html"
    context_object_name = "finances"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(month__icontains=search_query)
                | Q(year__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

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
            amount_spend=amount_spend
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
            amount_spend=amount_spend
        )
        
        return redirect("district-report-details", id=report.id)
    return render(request, "districts/expenses/edit_expense.html")



class SectionsListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = "districts/sections/sections.html"
    context_object_name = "sections"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(name__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["districts"] = District.objects.all()
        context["presbyters"] = User.objects.filter(role="Presbyter")
        return context
    

@login_required
@transaction.atomic
def new_section(request: HttpRequest):
    if request.method == "POST":
        presbyter = request.POST.get("presbyter")
        district = request.POST.get("district")
        name = request.POST.get("name")
        
        Section.objects.create(
            name=name,
            district_id=district,
            presbyter_id=presbyter
        )    
        return redirect("district-sections")
    return render(request, "districts/sections/new_section.html")


@login_required
def edit_section(request: HttpRequest):
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        presbyter = request.POST.get("presbyter")
        district = request.POST.get("district")
        name = request.POST.get("name")
        
        Section.objects.filter(id=section_id).update(
            presbyter_id=presbyter,
            district_id=district,
            name=name
        )
        
        return redirect("district-sections")
    return render(request, "districts/sections/edit_section.html")


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
        context["sections"] = Section.objects.all()
        context["gender_choices"] = GENDER_CHOICES
        return context
    

@login_required
@transaction.atomic
def new_presbyter(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        id_number = request.POST.get("id_number")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        
        email = email if email else f"{first_name}.{last_name}@gmail.com"
        
        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            id_number=id_number,
            email=email,
            role="Presbyter",
            phone_number=phone_number,
            username=email,
            gender=gender,
            address=address,
            city=city,
            country=country
        )    
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
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        
        email = email if email else f"{first_name}.{last_name}@gmail.com"
        
        user = User.objects.get(id=presbyter_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.id_number = id_number
        user.gender = gender
        user.address = address
        user.city = city
        user.country = country
        user.save()
        
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
                Q(id__icontains=search_query)
                | Q(section__name__icontains=search_query)
                | Q(month__icontains=search_query)
                | Q(year__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

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
    attendances = DistrictAttendance.objects.filter(report=report)
    total_children_attendance = sum(attendances.values_list("children", flat=True))
    total_adult_attendance = sum(attendances.values_list("adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

    finances = DistrictFinance.objects.filter(report=report)
    total_general_fund = sum(finances.values_list("general_fund", flat=True))
    total_sunday_school = sum(finances.values_list("sunday_school", flat=True))
    total_pastors_tithe = sum(finances.values_list("pastors_tithe", flat=True))
    total_easter = sum(finances.values_list("easter", flat=True))
    kenya_kids = sum(finances.values_list("kenya_kids", flat=True))
    special_offering = sum(finances.values_list("special_offering", flat=True))

    ten_percent_general_fund = Decimal(0.1) * total_general_fund
    five_percent_sunday_school = Decimal(0.05) * total_sunday_school
    five_percent_pastors_tithe = Decimal(0.05) * total_pastors_tithe
    half_easter_offering = Decimal(0.5) * total_easter

    district_total = ten_percent_general_fund + five_percent_sunday_school + five_percent_pastors_tithe + half_easter_offering + kenya_kids + special_offering
    district_grand_total = total_general_fund + total_sunday_school + total_pastors_tithe + total_easter + kenya_kids + special_offering

    sections = Section.objects.all()
    expenses = DistrictExpense.objects.filter(report=report)

    total_expenses = sum(expenses.values_list("amount_spend", flat=True))

    context = {
        "report": report,
        "attendances": attendances,
        "total_children_attendance": total_children_attendance,
        "total_adult_attendance": total_adult_attendance,
        "grand_total_attendance": grand_total_attendance,
        "finances": finances,
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
        "easter_total": total_easter
    }
    return render(request, "districts/report_details.html", context)


def district_report(request: HttpRequest, id: int):
    report = DistrictReport.objects.get(id=id)
    attendances = DistrictAttendance.objects.filter(report=report)
    total_children_attendance = sum(attendances.values_list("children", flat=True))
    total_adult_attendance = sum(attendances.values_list("adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

    finances = DistrictFinance.objects.filter(report=report)
    total_general_fund = sum(finances.values_list("general_fund", flat=True))
    total_sunday_school = sum(finances.values_list("sunday_school", flat=True))
    total_pastors_tithe = sum(finances.values_list("pastors_tithe", flat=True))
    total_pastors_fund = sum(finances.values_list("pastors_fund", flat=True))
    total_presbyter_tithe = sum(finances.values_list("presbyter_tithe", flat=True))
    total_easter = sum(finances.values_list("easter", flat=True))
    kenya_kids = sum(finances.values_list("kenya_kids", flat=True))
    special_offering = sum(finances.values_list("special_offering", flat=True))

    ten_percent_general_fund = Decimal(0.1) * total_general_fund
    five_percent_sunday_school = Decimal(0.05) * total_sunday_school
    five_percent_pastors_tithe = Decimal(0.05) * total_pastors_tithe
    half_easter_offering = Decimal(0.5) * total_easter

    district_total = ten_percent_general_fund + five_percent_sunday_school + five_percent_pastors_tithe + half_easter_offering + kenya_kids + special_offering
    district_grand_total = total_general_fund + total_sunday_school + total_presbyter_tithe + total_pastors_tithe + total_easter + kenya_kids + special_offering


    sections = Section.objects.all()
    expenses = DistrictExpense.objects.filter(report=report)
    total_expenses = sum(expenses.values_list("amount_spend", flat=True))

    non_tithe_totals = total_easter + special_offering + kenya_kids
    tithe_totals = total_presbyter_tithe + total_pastors_tithe
    revenue_totals = total_pastors_fund + total_general_fund + total_sunday_school

    context = {
        "report": report,
        "attendances": attendances,
        "total_children_attendance": total_children_attendance,
        "total_adult_attendance": total_adult_attendance,
        "grand_total_attendance": grand_total_attendance,
        "finances": finances,
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
        "non_tithe_totals": non_tithe_totals,
        "total_presbyter_tithe": total_presbyter_tithe,
        "total_pastors_tithe": total_pastors_tithe,
        "tithe_totals": round(tithe_totals, 2),
        "revenue_totals": round(revenue_totals, 2),
        "total_pastors_fund": round(total_pastors_fund, 2),
        "total_general_fund": round(total_general_fund, 2),
        "total_sunday_school": round(total_sunday_school, 2)
    }
    return render(request, "districts/district_report.html", context)


@login_required
@transaction.atomic
def capture_section_data(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        section = request.POST.get("section")
        
        general_fund = request.POST.get("general_fund")
        sunday_school = request.POST.get("sunday_school")

        pastors_tithe = request.POST.get("pastors_tithe")
        presbyter_tithe = request.POST.get("presbyter_tithe")
        
        easter = request.POST.get("easter")
        special_offering = request.POST.get("special_offering")
        kenya_kids = request.POST.get("kenya_kids")

        children = request.POST.get("children")
        adult = request.POST.get("adult")

        church_section = Section.objects.get(id=section)
        report = DistrictReport.objects.get(id=report_id)    

        DistrictAttendance.objects.create(
            report=report,
            district=church_section.district,
            section=church_section,
            year=report.year,
            month=report.month,
            children=children,
            adult=adult
        )

        DistrictFinance.objects.create(
            report=report,
            district=church_section.district,
            section=church_section,
            year=report.year,
            month=report.month,
            general_fund=general_fund,
            sunday_school=sunday_school,
            pastors_tithe=pastors_tithe,
            presbyter_tithe=presbyter_tithe,
            easter=easter,
            special_offering=special_offering,
            kenya_kids=kenya_kids
        )

        return redirect("district-report-details", id=report_id)
    return render(request, "districts/capture_section_data.html")


@login_required
@transaction.atomic
def new_report_data(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        section = request.POST.get("section")
        year = request.POST.get("year")
        month = request.POST.get("month")
        
        general_fund = request.POST.get("general_fund")
        sunday_school = request.POST.get("sunday_school")

        pastors_tithe = request.POST.get("pastors_tithe")
        presbyter_tithe = request.POST.get("presbyter_tithe")
        
        easter = request.POST.get("easter")
        special_offering = request.POST.get("special_offering")

        children = request.POST.get("children")
        adult = request.POST.get("adult")

        church_section = Section.objects.get(id=section)
        report = DistrictReport.objects.get(id=report_id)
                
        report = DistrictReport.objects.filter(id=report_id).update(
            district=church_section.district,
            section=church_section,
            year=year,
            month=month,
            general_fund=general_fund,
            sunday_school=sunday_school,
            pastors_tithe=pastors_tithe,
            presbyter_tithe=presbyter_tithe,
            easter=easter,
            special_offering=special_offering,
            children=children,
            adult=adult
        )    

        DistrictAttendance.objects.filter(report=report).update(
            report=report,
            district=church_section.district,
            section=church_section,
            year=year,
            month=month,
            children=children,
            adult=adult
        )

        DistrictFinance.objects.filter(report=report).create(
            report=report,
            district=church_section.district,
            section=church_section,
            year=year,
            month=month,
            general_fund=general_fund,
            sunday_school=sunday_school,
            pastors_tithe=pastors_tithe,
            presbyter_tithe=presbyter_tithe,
            easter=easter,
            special_offering=special_offering,
        )

        return redirect("reports")
    return render(request, "districts/edit_report.html")