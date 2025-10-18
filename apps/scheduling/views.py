from django.shortcuts import render

from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.scheduling.models import (
    Appointment, ChurchMeeting, ChurchMeetingAttendance,
    BurialRequest, BaptismRequest, PrayerRequest, MarriageRequest
)
# Create your views here.
# Create your views here.
date_today = datetime.now().date()

# Church Projects
class BurialRequestsListView(LoginRequiredMixin, ListView):
    model = BurialRequest
    template_name = "requests/burial/burial_requests.html"
    context_object_name = "requests"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(BurialRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(BurialRequest._meta.get_field("status").choices)
        return context


@login_required
@transaction.atomic
def new_burial_request(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        request_type = request.POST.get("request_type")
    

        BurialRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            request_type=request_type,
        )

        return redirect("burial-requests")
    return render(request, "requests/prayer/new_request.html")


@login_required
@transaction.atomic
def edit_burial_request(request):
    if request.method == "POST":
        burial_request_id = request.POST.get("burial_request_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        request_type = request.POST.get("request_type")
        status = request.POST.get("status")

        BurialRequest.objects.filter(id=burial_request_id).update(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            request_type=request_type,
            status=status,
        )

        return redirect("burial-requests")
    return render(request, "requests/prayer/edit_request.html")


@login_required
@transaction.atomic
def delete_burial_request(request):
    if request.method == "POST":
        burial_request_id = request.POST.get("burial_request_id")
        BurialRequest.objects.filter(id=burial_request_id).delete()
        return redirect("burial-requests")
    return render(request, "requests/prayer/delete_request.html")



class PrayerRequestsListView(LoginRequiredMixin, ListView):
    model = PrayerRequest
    template_name = "requests/prayer/prayer_requests.html"
    context_object_name = "requests"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(PrayerRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(PrayerRequest._meta.get_field("status").choices)
        return context


@login_required
@transaction.atomic
def new_prayer_request(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        request_type = request.POST.get("request_type")
    

        PrayerRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            request_type=request_type,
        )

        return redirect("prayer-requests")
    return render(request, "requests/prayer/new_request.html")


@login_required
@transaction.atomic
def edit_prayer_request(request):
    if request.method == "POST":
        prayer_request_id = request.POST.get("prayer_request_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        request_type = request.POST.get("request_type")
        status = request.POST.get("status")

        PrayerRequest.objects.filter(id=prayer_request_id).update(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            request_type=request_type,
            status=status,
        )

        return redirect("prayer-requests")
    return render(request, "requests/prayer/edit_request.html")


@login_required
@transaction.atomic
def delete_prayer_request(request):
    if request.method == "POST":
        prayer_request_id = request.POST.get("prayer_request_id")
        PrayerRequest.objects.filter(id=prayer_request_id).delete()
        return redirect("prayer-requests")
    return render(request, "requests/prayer/delete_request.html")



class BaptismRequestsListView(LoginRequiredMixin, ListView):
    model = BaptismRequest
    template_name = "requests/baptism/baptism_requests.html"
    context_object_name = "requests"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(BaptismRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(BaptismRequest._meta.get_field("status").choices)
        return context


@login_required
@transaction.atomic
def new_baptism_request(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        request_type = request.POST.get("request_type")
    

        BaptismRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            request_type=request_type,
        )

        return redirect("baptism-requests")
    return render(request, "requests/baptism/new_request.html")


@login_required
@transaction.atomic
def edit_baptism_request(request):
    if request.method == "POST":
        baptism_request_id = request.POST.get("baptism_request_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        request_type = request.POST.get("request_type")
        status = request.POST.get("status")

        BaptismRequest.objects.filter(id=baptism_request_id).update(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            request_type=request_type,
            status=status,
        )

        return redirect("prayer-requests")
    return render(request, "requests/baptism/edit_request.html")


@login_required
@transaction.atomic
def delete_baptism_request(request):
    if request.method == "POST":
        baptism_request_id = request.POST.get("baptism_request_id")
        BaptismRequest.objects.filter(id=baptism_request_id).delete()
        return redirect("baptism-requests")
    return render(request, "requests/baptism/delete_request.html")