from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q, Sum
from typing import Any
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator



from apps.sections.models import Section, SectionReport
from apps.membership.models import Branch
from apps.districts.models import District, KAGDistrictMonthlyReport, DistrictReport
from apps.users.models import User, Pastor
from apps.core.constants import MONTHS_LIST, YEARS_LIST, GENDER_CHOICES


class SectionReportsListView(LoginRequiredMixin, ListView):
    model = SectionReport
    template_name = "districts/section_reports/reports.html"
    context_object_name = "reports"
    paginate_by = 17

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(year__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["years"] = YEARS_LIST
        context["sections"] = Section.objects.all()
        return context
    


def section_report_details(request: HttpRequest, id: int):
    section_report = SectionReport.objects.get(id=id)

    section = Section.objects.get(id=section_report.section.id)
    churches = section.sectionbranches.all()

    pastors = Pastor.objects.filter(church__section=section)

    church_reports = KAGDistrictMonthlyReport.objects.filter(section=section).order_by("-created_at")

    yearly_sum = sum(list(church_reports.values_list("total_collected", flat=True)))


    context = {
        "section_report": section_report,
        "churches": churches,
        "pastors": pastors,
        "church_reports": church_reports,
        "months": MONTHS_LIST,
        "total_collected": yearly_sum,
    }
    return render(request, "districts/section_reports/report_details.html", context)
    
class SectionReportDetailView(View):
    template_name = "districts/section_reports/report_details.html"
    paginate_by = 10  # number of reports per page

    def get(self, request, id):
        # Retrieve section report and related data
        section_report = get_object_or_404(SectionReport, id=id)
        section = get_object_or_404(Section, id=section_report.section.id)
        churches = section.sectionbranches.all()
        pastors = Pastor.objects.filter(church__section=section)

        # Handle search query
        search_query = request.GET.get("search", "").strip()

        print(f"Search Query: {search_query}")

        church_reports = KAGDistrictMonthlyReport.objects.filter(section=section)

        if search_query:
            church_reports = church_reports.filter(
                Q(month__icontains=search_query)
            )

        church_reports = church_reports.order_by("-created_at")

        # Pagination
        paginator = Paginator(church_reports, self.paginate_by)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Calculate total collected for the (filtered) reports
        yearly_sum = (
            church_reports.aggregate(total_collected_sum=Sum("total_collected"))["total_collected_sum"]
            or 0
        )

        context = {
            "section_report": section_report,
            "churches": churches,
            "pastors": pastors,
            "church_reports": page_obj,  # paginated queryset
            "months": MONTHS_LIST,
            "total_collected": yearly_sum,
            "search_query": search_query,
            "is_paginated": page_obj.has_other_pages(),
            "page_obj": page_obj,
            "paginator": paginator,
        }

        return render(request, self.template_name, context)    

@login_required
@transaction.atomic
def new_section_reports(request: HttpRequest):
    if request.method == "POST":
    
        year = request.POST.get("year")
        
        sections = Section.objects.all()

        for section in sections:
            section_report = SectionReport.objects.filter(
                section=section, year=year
            ).first()

            if section_report:
                pass
            else:
                SectionReport.objects.create(
                    section=section,
                    year=year,
                    district=section.district
                )
        return redirect("section-reports")
    return render(request, "districts/section_reports/new_report.html")


@login_required
@transaction.atomic
def edit_section_report(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        section_id = request.POST.get("section_id")
        year = request.POST.get("year")
        
        section = Section.objects.get(id=section_id)

        SectionReport.objects.filter(id=report_id).update(
            section=section,
            year=year,
            district=section.district
        )
        return redirect("section-reports")
    return render(request, "districts/section_reports/edit_report.html")


@login_required
@transaction.atomic
def delete_section_report(request: HttpRequest):
    if request.method == "POST":
        report_id = request.POST.get("report_id")

        report = SectionReport.objects.get(id=report_id)
        report.delete()
        return redirect("section-reports")

    return render(request, "districts/section_reports/delete_report.html")