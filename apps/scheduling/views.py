from django.shortcuts import render

from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.scheduling.models import ChurchMemberRequest

from apps.core.constants import get_month_name, get_month_number
# Create your views here.
# Create your views here.
date_today = datetime.now().date()

# Church Projects
class BurialRequestsListView(LoginRequiredMixin, ListView):
    model = ChurchMemberRequest
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
        return queryset.filter(category="Burial").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(ChurchMemberRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(ChurchMemberRequest._meta.get_field("status").choices)
        context["genders"] = dict(ChurchMemberRequest._meta.get_field("gender").choices)
        return context



class PrayerRequestsListView(LoginRequiredMixin, ListView):
    model = ChurchMemberRequest
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
        return queryset.filter(category="Prayer").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(ChurchMemberRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(ChurchMemberRequest._meta.get_field("status").choices)
        context["genders"] = dict(ChurchMemberRequest._meta.get_field("gender").choices)
        return context


class BaptismRequestsListView(LoginRequiredMixin, ListView):
    model = ChurchMemberRequest
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
        return queryset.filter(category="Baptism").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(ChurchMemberRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(ChurchMemberRequest._meta.get_field("status").choices)
        context["genders"] = dict(ChurchMemberRequest._meta.get_field("gender").choices)
        return context



class MarriageRequestsListView(LoginRequiredMixin, ListView):
    model = ChurchMemberRequest
    template_name = "requests/marriage/marriage_requests.html"
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
        return queryset.filter(category="Wedding").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_types"] = dict(ChurchMemberRequest._meta.get_field("request_type").choices)
        context["request_statuses"] = dict(ChurchMemberRequest._meta.get_field("status").choices)
        return context



@login_required
@transaction.atomic
def new_member_request(request: HttpRequest):
    if request.method == "POST":
        category = request.POST.get("category")
    
        ChurchMemberRequest.objects.create(
            category=category,
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            gender = request.POST.get("gender"),
            request_type = request.POST.get("request_type"),
            status = request.POST.get("status", "Pending"),
            request_date = request.POST.get("request_date"),
            phone_number = request.POST.get("phone_number"),
            bride_first_name = request.POST.get("bride_first_name"),
            bride_last_name = request.POST.get("bride_last_name"),
            groom_first_name = request.POST.get("groom_first_name"),
            groom_last_name = request.POST.get("groom_last_name"),
            wedding_date = request.POST.get("wedding_date"),
            wedding_location = request.POST.get("wedding_location")
        )

        if category.lower() == "burial":
            return redirect("burial-requests")
        elif category.lower() == "prayer":
            return redirect("prayer-requests")
        elif category.lower() == "wedding":
            return redirect("marriage-requests")
        return redirect("baptism-requests")
    return render(request, "requests/baptism/new_request.html")


@login_required
@transaction.atomic
def edit_member_request(request: HttpRequest):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        category = request.POST.get("category")

        ChurchMemberRequest.objects.filter(id=request_id).update(
            category=category,
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            gender = request.POST.get("gender"),
            request_type = request.POST.get("request_type"),
            status = request.POST.get("status"),
            request_date = request.POST.get("request_date"),
            phone_number = request.POST.get("phone_number"),
            bride_first_name = request.POST.get("bride_first_name"),
            bride_last_name = request.POST.get("bride_last_name"),
            groom_first_name = request.POST.get("groom_first_name"),
            groom_last_name = request.POST.get("groom_last_name"),
            wedding_date = request.POST.get("wedding_date"),
            wedding_location = request.POST.get("wedding_location")
        )

        if category.lower() == "burial":
            return redirect("burial-requests")
        elif category.lower() == "prayer":
            return redirect("prayer-requests")
        elif category.lower() == "wedding":
            return redirect("marriage-requests")
        return redirect("baptism-requests")
    return render(request, "requests/baptism/edit_request.html")


@login_required
@transaction.atomic
def delete_member_request(request: HttpRequest):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        category = request.POST.get("category")
        ChurchMemberRequest.objects.filter(id=request_id).delete()
        if category.lower() == "burial":
            return redirect("burial-requests")
        elif category.lower() == "prayer":
            return redirect("prayer-requests")
        elif category.lower() == "wedding":
            return redirect("marriage-requests")
        return redirect("baptism-requests")
    return render(request, "requests/baptism/delete_request.html")

