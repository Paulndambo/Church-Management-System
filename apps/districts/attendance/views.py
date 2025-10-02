from django.http import HttpRequest
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.db import transaction
from typing import Dict, Any


from apps.core.constants import get_month_name
from apps.districts.models import (
    District,
    DistrictAttendance,
    DistrictMeeting,
    DistrictMeetingAttendace,
)


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


class DistrictMeetingListView(LoginRequiredMixin, ListView):
    model = DistrictMeeting
    template_name = "districts/meetings/meetings.html"
    context_object_name = "meetings"
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
        context["districts"] = District.objects.all()
        return context


@login_required
@transaction.atomic
def district_meeting_details(request: HttpRequest, id: int):
    meeting = DistrictMeeting.objects.get(id=id)
    attendants = meeting.districtmeetingattendances.all()

    context: Dict[str, Any] = {
        "meeting": meeting,
        "attendants": attendants,
        "roles": [
            "Church Member",
            "Pastor",
            "Treasurer",
            "Secretary",
            "Presbyter",
            "District Supritendant",
        ],
        "statuses": ["Present", "Absent"],
    }
    return render(request, "districts/meetings/district_meeting_details.html", context)


@login_required
@transaction.atomic
def new_district_meeting(request: HttpRequest):
    if request.method == "POST":
        district = District.objects.get(id=1)
        meeting_date = request.POST.get("meeting_date")

        date_obj = datetime.strptime(meeting_date, "%Y-%m-%d").date()

        meeting = DistrictMeeting.objects.create(
            district=district, meeting_date=meeting_date
        )
        meeting.month = get_month_name(date_obj.month)
        meeting.year = date_obj.year
        meeting.save()

        return redirect("district-meeting-details", id=meeting.id)
    return render(request, "districts/meetings/new_meeting.html")


class DistrictMeetingAttendanceListView(LoginRequiredMixin, ListView):
    model = DistrictMeetingAttendace
    template_name = "districts/meetings/meeting_attendances.html"
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


@login_required
def create_meeting_attendant(request: HttpRequest):
    if request.method == "POST":
        meeting_id = request.POST.get("meeting_id")
        full_name = request.POST.get("full_name")
        status = request.POST.get("status")
        role = request.POST.get("role")

        meeting = DistrictMeeting.objects.get(id=meeting_id)

        DistrictMeetingAttendace.objects.create(
            meeting=meeting,
            full_name=full_name,
            status=status,
            month=meeting.month,
            year=meeting.year,
            role=role,
            recorded_by=request.user
        )
        return redirect("district-meeting-details", id=meeting.id)
    return render(request, "districts/meetings/create_attendant.html")


@login_required
def edit_meeting_attendant(request: HttpRequest):
    if request.method == "POST":
        attendant_id = request.POST.get("attendant_id")
        meeting_id = request.POST.get("meeting_id")
        full_name = request.POST.get("full_name")
        status = request.POST.get("status")
        role = request.POST.get("role")

        meeting = DistrictMeeting.objects.get(id=meeting_id)

        DistrictMeetingAttendace.objects.filter(id=attendant_id).update(
            meeting=meeting,
            full_name=full_name,
            status=status,
            month=meeting.month,
            year=meeting.year,
            role=role,
            recorded_by=request.user
        )
        return redirect("district-meeting-details", id=meeting.id)
    return render(request, "districts/meetings/edit_attendant.html")


@login_required
@transaction.atomic
def mark_district_meeting_attendance(request: HttpRequest, id: int):
    attendance = DistrictMeetingAttendace.objects.get(id=id)
    attendance.present = True
    attendance.save()

    return redirect("district-meeting-details", id=attendance.meeting.id)
    return render(request, "districts/meetings/mark_attendance.html")
