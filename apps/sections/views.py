from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q
from typing import Any
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from apps.sections.models import Section, SectionReport
from apps.membership.models import Branch
from apps.districts.models import District, KAGDistrictMonthlyReport, DistrictReport
from apps.users.models import User, Pastor
from apps.core.constants import MONTHS_LIST, YEARS_LIST, GENDER_CHOICES

# Create your views here.
class SectionsListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = "districts/sections/sections.html"
    context_object_name = "sections"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) | Q(name__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["districts"] = District.objects.all()
        context["presbyters"] = User.objects.filter(role="Presbyter")
        return context


@login_required
def section_details(request: HttpRequest, id: int):
    search_query = request.GET.get("search", "")

    section = Section.objects.get(id=id)
    churches = Branch.objects.filter(section=section)

    lead_pastors_count = Pastor.objects.filter(church__section=section).filter(pastor_role="Lead Pastor").count()
    associate_pastors_count = Pastor.objects.filter(church__section=section).filter(pastor_role="Pastor Associate").count()

    church_reports = KAGDistrictMonthlyReport.objects.filter(section=section)

    section_churches_count = Branch.objects.filter(section=section).count()

    reports_to_show = church_reports[:section_churches_count]

    context = {
        "section": section,
        "branches": churches,
        "months": MONTHS_LIST,
        "years": YEARS_LIST,
        "church_reports": reports_to_show,
        "lead_pastors_count": lead_pastors_count,
        "associate_pastors_count": associate_pastors_count,
    }
    return render(request, "districts/sections/section_details.html", context)


@login_required
@transaction.atomic
def new_section(request: HttpRequest):
    if request.method == "POST":
        district = request.POST.get("district")
        name = request.POST.get("name")

        Section.objects.create(name=name, district_id=district)
        return redirect("district-sections")
    return render(request, "districts/sections/new_section.html")


@login_required
def edit_section(request: HttpRequest):
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        district = request.POST.get("district")
        name = request.POST.get("name")

        Section.objects.filter(id=section_id).update(district_id=district, name=name)

        return redirect("district-sections")
    return render(request, "districts/sections/edit_section.html")



@login_required
def branch_details(request: HttpRequest, id: int):
    branch = Branch.objects.get(id=id)

    section_reports = KAGDistrictMonthlyReport.objects.filter(report=branch.section)

    total_children_attendance = sum(section_reports.values_list("children", flat=True))
    total_adult_attendance = sum(section_reports.values_list("adult", flat=True))
    grand_total_attendance = total_adult_attendance + total_children_attendance

    total_general_fund = sum(section_reports.values_list("general_fund", flat=True))
    total_sunday_school = sum(section_reports.values_list("sunday_school", flat=True))
    total_pastors_tithe = sum(section_reports.values_list("pastors_tithe", flat=True))
    total_pastors_fund = sum(section_reports.values_list("pastors_fund", flat=True))
    total_presbyter_tithe = sum(
        section_reports.values_list("presbyter_tithe", flat=True)
    )
    total_easter = sum(section_reports.values_list("easter", flat=True))
    kenya_kids = sum(section_reports.values_list("kenya_kids", flat=True))
    special_offering = sum(section_reports.values_list("special_offering", flat=True))

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

    total_kagdom = sum(section_reports.values_list("kagdom", flat=True))
    total_resource_mobilisation = sum(
        section_reports.values_list("resource_mobilisation", flat=True)
    )
    total_district_missions = sum(
        section_reports.values_list("district_missions", flat=True)
    )
    total_church_support = sum(section_reports.values_list("church_support", flat=True))
    total_church_welfare = sum(section_reports.values_list("church_welfare", flat=True))

    total_additionals = (
        total_kagdom
        + total_resource_mobilisation
        + total_district_missions
        + total_church_support
    )

    context = {
        "branch": branch,
        "district_reports": district_reports
    }

    return render(request, "district/branches/branch_details.html", context)


@login_required
@transaction.atomic
def capture_church_data(request: HttpRequest):
    if request.method == "POST":
        church_id = request.POST.get("church")
        report_id = request.POST.get("report_id")

        year = request.POST.get("year")
        month = request.POST.get("month")
        
        general_fund = request.POST.get("general_fund")
        sunday_school = request.POST.get("sunday_school")

        total_collected = request.POST.get("total_collected")
        pastor = request.POST.get("pastor")

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

        print("**************Details*****************")
        #print(f"Section ID: {section_id}")
        print(f"Year: {year}")
        print(f"Month: {month}")
        print("**************Details*****************")

        section_report = SectionReport.objects.get(id=report_id)
        church = Branch.objects.get(id=church_id)
        

        report = DistrictReport.objects.filter(year=year, month=month).first()

        if not report:
            report = DistrictReport.objects.create(
                district=church.section.district,
                month=month,
                year=section_report.year
            )

        KAGDistrictMonthlyReport.objects.create(
            report=report,
            church=church,
            pastor_id=pastor,
            total_collected=total_collected,
            district=church.section.district,
            section=church.section,
            section_report=section_report,
            year=section_report.year,
            month=month,
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
            pastors_fund=pastors_fund,
        )

        return redirect("section-report-detail", id=report_id)
    return render(request, "districts/capture_church_data.html")


@login_required
@transaction.atomic
def edit_section_data(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        section_id = request.POST.get("section_id")
        general_fund = request.POST.get("general_fund")
        sunday_school = request.POST.get("sunday_school")
        year = request.POST.get("year")
        month = request.POST.get("month")
        total_collected = request.POST.get("total_collected")
        pastor = request.POST.get("pastor")

        church_id = request.POST.get("church_id")

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

        print("**************Details*****************")
        print(f"Section ID: {section_id}")
        print(f"Year: {year}")
        print(f"Month: {month}")
        print("**************Details*****************")

        section_report = SectionReport.objects.filter(section__id=section_id, year=year).first()
        

        KAGDistrictMonthlyReport.objects.filter(id=report_id).update(
            children=children,
            adult=adult,
            church_id=church_id,
            pastor_id=pastor,
            total_collected=total_collected,
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
            year=section_report.year,
            month=month,
            church_support=church_support,
            church_welfare=church_welfare,
            pastors_fund=pastors_fund,
        )

        return redirect("section-report-detail", id=section_report.id)
    return render(request, "districts/edit_section_data.html")


@login_required
@transaction.atomic
def delete_church_data(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        church_report_id = request.POST.get("church_report_id")

        KAGDistrictMonthlyReport.objects.filter(id=church_report_id).delete()

        return redirect("section-report-detail", id=report_id)
    return render(request, "districts/section_reports/delete_report.html")