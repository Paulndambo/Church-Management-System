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
from apps.districts.models import (
    District, DistrictAttendance, DistrictFinance, 
    DistrictReport, DistrictExpense,
    DistrictMeeting, DistrictMeetingAttendace, SectionReport
)
from apps.membership.models import Branch

# Create your views here.
def district_home(request: HttpRequest):
    return render(request, "districts/home.html")

    

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
        district = request.POST.get("district")
        name = request.POST.get("name")
        
        Section.objects.create(
            name=name,
            district_id=district
        )    
        return redirect("district-sections")
    return render(request, "districts/sections/new_section.html")


@login_required
def edit_section(request: HttpRequest):
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        district = request.POST.get("district")
        name = request.POST.get("name")
        
        Section.objects.filter(id=section_id).update(
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
    section_reports = SectionReport.objects.filter(report=report)
  
    total_children_attendance = sum(section_reports.values_list("children", flat=True))
    total_adult_attendance = sum(section_reports.values_list("adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

    finances = DistrictFinance.objects.filter(report=report)
    total_general_fund = sum(section_reports.values_list("general_fund", flat=True))
    total_sunday_school = sum(section_reports.values_list("sunday_school", flat=True))
    total_pastors_tithe = sum(section_reports.values_list("pastors_tithe", flat=True))
    total_pastors_fund = sum(section_reports.values_list("pastors_fund", flat=True))
    total_presbyter_tithe = sum(section_reports.values_list("presbyter_tithe", flat=True))
    total_easter = sum(section_reports.values_list("easter", flat=True))
    kenya_kids = sum(section_reports.values_list("kenya_kids", flat=True))
    special_offering = sum(section_reports.values_list("special_offering", flat=True))

    ten_percent_general_fund = Decimal(0.1) * total_general_fund
    five_percent_sunday_school = Decimal(0.05) * total_sunday_school
    five_percent_pastors_tithe = Decimal(0.05) * total_pastors_tithe
    half_easter_offering = Decimal(0.5) * total_easter

    district_total = ten_percent_general_fund + five_percent_sunday_school + five_percent_pastors_tithe + half_easter_offering + kenya_kids + special_offering
    district_grand_total = total_general_fund + total_sunday_school + total_pastors_tithe + total_easter + kenya_kids + special_offering

    sections = Section.objects.all()
    expenses = DistrictExpense.objects.filter(report=report)

    total_expenses = sum(expenses.values_list("amount_spend", flat=True))

    total_kagdom = sum(section_reports.values_list("kagdom", flat=True))
    total_resource_mobilisation = sum(section_reports.values_list("resource_mobilisation", flat=True))
    total_district_missions= sum(section_reports.values_list("district_missions", flat=True))
    total_church_support = sum(section_reports.values_list("church_support", flat=True))
    total_church_welfare = sum(section_reports.values_list("church_welfare", flat=True))

    total_additionals = total_kagdom + total_resource_mobilisation + total_district_missions + total_church_support

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
        "total_kagdom": total_kagdom,
        "total_resource_mobilisation": total_resource_mobilisation,
        "total_district_missions": total_district_missions,
        "total_church_support": total_church_support,
        "total_additionals": total_additionals,
        "total_presbyter_tithe": total_presbyter_tithe
    }
    return render(request, "districts/report_details.html", context)


def district_report(request: HttpRequest, id: int):
    report = DistrictReport.objects.get(id=id)
    section_reports = SectionReport.objects.filter(report=report)
  
    total_children_attendance = sum(section_reports.values_list("children", flat=True))
    total_adult_attendance = sum(section_reports.values_list("adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

    finances = DistrictFinance.objects.filter(report=report)
    total_general_fund = sum(section_reports.values_list("general_fund", flat=True))
    total_sunday_school = sum(section_reports.values_list("sunday_school", flat=True))
    total_pastors_tithe = sum(section_reports.values_list("pastors_tithe", flat=True))
    total_pastors_fund = sum(section_reports.values_list("pastors_fund", flat=True))
    total_presbyter_tithe = sum(section_reports.values_list("presbyter_tithe", flat=True))
    total_easter = sum(section_reports.values_list("easter", flat=True))
    kenya_kids = sum(section_reports.values_list("kenya_kids", flat=True))
    special_offering = sum(section_reports.values_list("special_offering", flat=True))

    ten_percent_general_fund = Decimal(0.1) * total_general_fund
    five_percent_sunday_school = Decimal(0.05) * total_sunday_school
    five_percent_pastors_tithe = Decimal(0.05) * total_pastors_tithe
    half_easter_offering = Decimal(0.5) * total_easter

    district_total = ten_percent_general_fund + five_percent_sunday_school + five_percent_pastors_tithe + half_easter_offering + kenya_kids + special_offering
    district_grand_total = total_general_fund + total_sunday_school + total_pastors_tithe + total_easter + kenya_kids + special_offering

    sections = Section.objects.all()
    expenses = DistrictExpense.objects.filter(report=report)

    total_expenses = sum(expenses.values_list("amount_spend", flat=True))

    total_kagdom = sum(section_reports.values_list("kagdom", flat=True))
    total_resource_mobilisation = sum(section_reports.values_list("resource_mobilisation", flat=True))
    total_district_missions= sum(section_reports.values_list("district_missions", flat=True))
    total_church_support = sum(section_reports.values_list("church_support", flat=True))
    total_church_welfare = sum(section_reports.values_list("church_welfare", flat=True))

    total_additionals = total_kagdom + total_resource_mobilisation + total_district_missions + total_church_support

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
        "total_kagdom": total_kagdom,
        "total_resource_mobilisation": total_resource_mobilisation,
        "total_district_missions": total_district_missions,
        "total_church_support": total_church_support,
        "total_additionals": total_additionals,
        "total_presbyter_tithe": total_presbyter_tithe
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

        kagdom = request.POST.get("kagdom")
        church_support = request.POST.get("church_support")
        resource_mobilisation = request.POST.get("resource_mobilisation")
        district_missions = request.POST.get("district_missions")
        pastors_fund = request.POST.get("pastors_fund")
        church_welfare = request.POST.get("church_welfare")

        church_section = Section.objects.get(id=section)
        report = DistrictReport.objects.get(id=report_id)    

        SectionReport.objects.create(
            report=report,
            district=church_section.district,
            section=church_section,
            year=report.year,
            month=report.month,
            children=children,
            adult=adult,
            general_fund=general_fund,
            sunday_school=sunday_school,
            pastors_tithe=pastors_tithe,
            presbyter_tithe=presbyter_tithe,
            easter=easter,
            special_offering=special_offering,
            kenya_kids=kenya_kids,
            district_missions=district_missions,
            resource_mobilisation=resource_mobilisation,
            kagdom=kagdom,
            church_support=church_support,
            church_welfare=church_welfare,
            pastors_fund=pastors_fund
        )

        return redirect("district-report-details", id=report_id)
    return render(request, "districts/capture_section_data.html")


@login_required
def district_branches(request: HttpRequest):
    branches = Branch.objects.all().order_by("-created_at")
    sections = Section.objects.all()
    context = {
        "branches": branches,
        "sections": sections
    }
    return render(request, "districts/branches/branches.html", context)


@login_required
def new_district_branch(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        town = request.POST.get("town")
        location = request.POST.get("location")
        section = request.POST.get("section")

         
        branch = Branch.objects.create(
            section_id=section,
            name=name,
            location=location,
            town=town
        )

        return redirect("district-churches")
    return render(request, "districts/branches/new_branch.html")
