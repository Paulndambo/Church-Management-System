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
    ChurchMeeting, Appointment
)


# Church Appointments
class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "scheduling/appointments/appointments.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(status__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = ["Accepted", "Declined", "Completed", "Cancelled", "Pending"]
        context["appointment_types"] = ["Member Appointment", "Non-Member Appointment"]
        return context


@login_required
@transaction.atomic
def new_appointment(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        appointment_date = request.POST.get("appointment_date")
        appointment_type = request.POST.get("appointment_type")
        town = request.POST.get("town")
        country = request.POST.get("country")
        gender = request.POST.get("gender")
        status = request.POST.get("status")

        formatted_date = format_datetime(appointment_date)
        month = get_month_name(formatted_date.month)
        
        Appointment.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            appointment_date=appointment_date,
            appointment_type=appointment_type,
            town=town,
            country=country,
            gender=gender,
            recorded_by=request.user,
            month=month,
            year=formatted_date.year,
            church=request.user.church,
            status=status,
        )

        return redirect("appointments")
    return render(request, "scheduling/appointments/new_appointment.html")


@login_required
@transaction.atomic
def edit_appointment(request: HttpRequest):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        appointment_date = request.POST.get("appointment_date")
        town = request.POST.get("town")
        country = request.POST.get("country")
        gender = request.POST.get("gender")
        status = request.POST.get("status")
        appointment_type = request.POST.get("appointment_type")

        formatted_date = format_datetime(appointment_date)
        month = get_month_name(formatted_date.month)
        
        Appointment.objects.filter(id=appointment_id).update(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            appointment_date=appointment_date,
            appointment_type=appointment_type,
            town=town,
            country=country,
            gender=gender,
            recorded_by=request.user,
            month=month,
            year=formatted_date.year,
            church=request.user.church,
            status=status,
        )


        return redirect("appointments")
    return render(request, "scheduling/appointments/edit_appointment.html")



@login_required
@transaction.atomic
def approve_or_decline(request: HttpRequest):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        appointment_date = request.POST.get("appointment_date")
        status = request.POST.get("status")  # 'approve' or 'decline'
        Appointment.objects.filter(id=appointment_id).update(
            status=status,
            appointment_date=appointment_date,
            recorded_by=request.user,
        )
        return redirect("appointments")
    return render(request, "scheduling/appointments/mark_appointment.html")