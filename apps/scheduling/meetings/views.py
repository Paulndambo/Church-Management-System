from django.shortcuts import render
from typing import Any, Dict, List
from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.constants import get_month_name, format_datetime

from apps.scheduling.models import (
    ChurchMeeting, ChurchMeetingAttendance, Appointment
)
from apps.core.models import ChurchRole
# Create your views here.
# Create your views here.
date_today = datetime.now().date()

# Church Projects
class ChurchMeetingsListView(LoginRequiredMixin, ListView):
    model = ChurchMeeting
    template_name = "scheduling/meetings/church_meetings.html"
    context_object_name = "meetings"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meeting_statuses"] = ["Scheduled", "Completed", "Cancelled"]
        return context


@login_required
@transaction.atomic
def new_church_meeting(request: HttpRequest):
    if request.method == "POST":
        title = request.POST.get("title")
        meeting_date = request.POST.get("meeting_date")
        meeting_location = request.POST.get("meeting_location")
        status = request.POST.get("status")

        formatted_date = format_datetime(meeting_date)
        month = get_month_name(formatted_date.month)
        
        ChurchMeeting.objects.create(
            title=title,
            meeting_date=meeting_date,
            meeting_location=meeting_location,
            recorded_by=request.user,
            month=month,
            year=formatted_date.year,
            church=request.user.church,
            status=status,
        )

        return redirect("church-meetings")
    return render(request, "scheduling/meetings/new_church_meeting.html")


@login_required
@transaction.atomic
def edit_church_meeting(request: HttpRequest):
    if request.method == "POST":
        meeting_id = request.POST.get("meeting_id")
        title = request.POST.get("title")
        meeting_date = request.POST.get("meeting_date")
        meeting_location = request.POST.get("meeting_location")
        status = request.POST.get("status")

        
        formatted_date = format_datetime(meeting_date)
        month = get_month_name(formatted_date.month)
        
        ChurchMeeting.objects.filter(id=meeting_id).update(
            title=title,
            meeting_date=meeting_date,
            meeting_location=meeting_location,
            recorded_by=request.user,
            month=month,
            year=formatted_date.year,
            church=request.user.church,
            status=status,
        )

        return redirect("church-meetings")
    return render(request, "scheduling/meetings/edit_church_meeting.html")



@login_required
@transaction.atomic
def delete_church_meeting(request: HttpRequest):
    if request.method == "POST":
        meeting_id = request.POST.get("meeting_id")
        ChurchMeeting.objects.filter(id=meeting_id).delete()
        return redirect("church-meetings")
    return render(request, "scheduling/meetings/delete_church_meeting.html")


@login_required
def church_meeting_detail(request: HttpRequest, id: int):
    meeting = ChurchMeeting.objects.get(id=id)
    attendances = ChurchMeetingAttendance.objects.filter(meeting=meeting)
    context: Dict[str, Any] = {
        "meeting": meeting,
        "attendances": attendances,
        "attendances_count": attendances.count(),
        "genders": ["Male", "Female"],
        "roles": ChurchRole.objects.filter(church=request.user.church),
        "statuses": ["Present", "Excused", "Late", "Absent with Apology", "Absent without Apology"],

    }
    return render(request, "scheduling/meetings/church_meeting_detail.html", context)


@login_required
@transaction.atomic
def add_church_meeting_attendance(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        status = request.POST.get("status")
        role = request.POST.get("role")
        meeting_id = request.POST.get("meeting_id")
        gender = request.POST.get("gender")

        meeting = ChurchMeeting.objects.get(id=meeting_id)
        meeting_date = meeting.meeting_date
        
        month = get_month_name(meeting_date.month)

        ChurchMeetingAttendance.objects.create(
            meeting_id=meeting_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            status=status,
            role=role,
            recorded_by=request.user,
            month=month,
            year=meeting_date.year,
            church=request.user.church,
            gender=gender
        )

        return redirect("church-meeting-detail", id=meeting_id)
    return render(request, "scheduling/meetings/new_attendance.html")



@login_required
@transaction.atomic
def edit_church_meeting_attendance(request: HttpRequest):
    if request.method == "POST":
        attendance_id = request.POST.get("attendance_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        status = request.POST.get("status")
        role = request.POST.get("role")
        meeting_id = request.POST.get("meeting_id")
        gender = request.POST.get("gender")

        meeting = ChurchMeeting.objects.get(id=meeting_id)
        meeting_date = meeting.meeting_date
        

        month = get_month_name(meeting_date.month)

        ChurchMeetingAttendance.objects.filter(id=attendance_id).update(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            status=status,
            role=role,
            recorded_by=request.user,
            month=month,
            year=meeting_date.year,
            church=request.user.church,
            gender=gender
        )

        return redirect("church-meeting-detail", id=meeting_id)
    return render(request, "scheduling/meetings/edit_attendance.html")


@login_required
@transaction.atomic
def delete_church_meeting_attendance(request: HttpRequest):
    if request.method == "POST":
        attendance_id = request.POST.get("attendance_id")
        meeting_id = request.POST.get("meeting_id")
        ChurchMeetingAttendance.objects.filter(id=attendance_id).delete()
        return redirect("church-meeting-detail", id=meeting_id)
    return render(request, "scheduling/meetings/delete_attendance.html")
