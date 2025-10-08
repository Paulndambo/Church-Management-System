from datetime import datetime

# Create your views here.
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q
from typing import Any
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import calendar

from apps.membership.models import Branch, Member


from apps.attendances.models import (
    ServiceAttendanceMetric,
    ServiceAttendance,
    ChurchService,
)

from apps.core.models import UserActionLog


### Services Management
@login_required
def church_services(request: HttpRequest):
    services = ChurchService.objects.all().order_by("-created_at")

    context: dict[str, Any] = {
        "services": services,
        "service_days": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
    }
    return render(request, "services/services.html", context)


@login_required
def new_church_service(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        starts_at = request.POST.get("starts_at")
        ends_at = request.POST.get("ends_at")
        service_day = request.POST.get("service_day")

        ChurchService.objects.create(
            name=name, service_day=service_day, starts_at=starts_at, ends_at=ends_at
        )

        return redirect("church-services")
    return render(request, "services/new_service.html")


@login_required
def edit_church_service(request: HttpRequest):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        name = request.POST.get("name")
        starts_at = request.POST.get("starts_at")
        ends_at = request.POST.get("ends_at")
        service_day = request.POST.get("service_day")

        service = ChurchService.objects.get(id=service_id)
        service.name = name
        service.starts_at = starts_at
        service.ends_at = ends_at
        service.service_day = service_day
        service.save()
        return redirect("church-services")
    return render(request, "services/edit_service.html")


@login_required
def delete_church_service(request: HttpRequest):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        service = ChurchService.objects.get(id=service_id)
        service.delete()
        return redirect("church-services")
    return render(request, "services/delete_service.html")


### Service Attendance Metrics
class ServiceAttendanceMetricsListView(LoginRequiredMixin, ListView):
    model = ServiceAttendanceMetric
    template_name = "attendances/service_attendances.html"
    context_object_name = "attendances"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(branch__name__icontains=search_query)
                | Q(month__icontains=search_query)
                | Q(year__icontains=search_query)
            )
        return queryset.select_related("branch", "service").order_by("-created_at")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        context["branches"] = Branch.objects.all()
        context["services"] = ChurchService.objects.all()
        return context


@login_required
@transaction.atomic
def record_service_attendance(request: HttpRequest) -> Any:
    if request.method == "POST":
        branch_id = request.POST.get("branch")
        service_id = request.POST.get("service")
        service_date = request.POST.get("service_date")
        total_present = request.POST.get("total_present")
        gender = request.POST.get("gender")

        date_obj = datetime.strptime(service_date, "%Y-%m-%d").date()

        branch = Branch.objects.get(id=branch_id)
        service = ChurchService.objects.get(id=service_id)

        metric_log = ServiceAttendanceMetric.objects.filter(
            branch=branch, service=service, service_date=date_obj, gender=gender
        ).first()

        if metric_log:
            metric_log.total_present += int(total_present)
            metric_log.save()
        else:
            metric_log = ServiceAttendanceMetric.objects.create(
                branch=branch,
                service=service,
                total_present=total_present,
                service_date=date_obj,
                gender=gender,
                recorded_by=request.user
            )
            metric_log.month = calendar.month_name[date_obj.month]
            metric_log.year = date_obj.year
            metric_log.save()

        UserActionLog.objects.create(
            user=request.user,
            action_type="Record Service Attendance",
            action_description=f"Recorded attendance for {service.name} on {service_date} at {branch.name}",
            metadata={
                "branch_id": branch.id,
                "branch_name": branch.name,
                "service_id": service.id,
                "service_name": service.name,
                "service_date": service_date,
                "total_present": total_present,
                "recorded_by": request.user.username
            },
        )
        if request.user.role == "Church Usher":
            return redirect("usher-home")
        return redirect("service-attendances")

    return render(request, "attendances/record_service_attendance.html")


### Church Attendance Management
class ServiceAttendaceView(LoginRequiredMixin, ListView):
    model = ServiceAttendance
    template_name = "attendances/attendances.html"
    context_object_name = "attendances"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(user__id_number__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs: dict[str, Any]):
        context = super().get_context_data(**kwargs)
        context["church_services"] = ChurchService.objects.all()
        context["members"] = Member.objects.all()
        return context


@login_required
@transaction.atomic
def new_attendance(request: HttpRequest):
    if request.method == "POST":
        member = request.POST.get("member")
        service = request.POST.get("church_service")
        status = request.POST.get("status")

        member = Member.objects.get(id=member)
        service = ChurchService.objects.get(id=service)

        attendance = ServiceAttendance.objects.create(
            member=member, service=service, status=status, gender=member.user.gender
        )

        metric_log = ServiceAttendanceMetric.objects.filter(
            branch=member.branch,
            service=service,
            service_date=attendance.created_at.date(),
        ).first()

        if metric_log:
            if status == "Present":
                metric_log.total_present += 1
            metric_log.save()
        else:
            total_present = 1 if status == "Present" else 0
            metric_log = ServiceAttendanceMetric.objects.create(
                branch=member.branch,
                service=service,
                total_present=total_present,
                service_date=attendance.created_at.date(),
                gender=member.user.gender,
                recorded_by=request.user
            )
            metric_log.month = calendar.month_name[metric_log.service_date.month]
            metric_log.year = metric_log.service_date.year
            metric_log.save()

        UserActionLog.objects.create(
            user=request.user,
            action_type="Create Attendance",
            action_description=f"Created attendance record for {member.user.get_full_name()} for {service.name}",
            metadata={
                "member_id": member.id,
                "member_name": member.user.get_full_name(),
                "service_id": service.id,
                "service_name": service.name,
                "status": status,
                "recorded_by": request.user.username
            },
        )
        return redirect("member-attendances")
    return render(request, "attendances/new_attendance.html")
