from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from decimal import Decimal

from apps.notifications.models import UserMessage, UserMessageRecipient, SMSSubscription


# Create your views here.
class UserMessageListView(LoginRequiredMixin, ListView):
    model = UserMessage
    template_name = "notifications/notifications.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) | Q(title__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def create_user_message(request: HttpRequest):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        message_type = request.POST.get("message_type")
        scheduled = request.POST.get("scheduled")
        scheduled_time = request.POST.get("scheduled_time") if scheduled else None

        UserMessage.objects.create(
            title=title,
            message=message,
            message_type=message_type,
            scheduled=scheduled,
            scheduled_time=scheduled_time,
            created_by=request.user,
        )
        return redirect("notifications")
    return render(request, "notifications/create_message.html")


@login_required
def edit_user_message(request: HttpRequest):
    if request.method == "POST":
        message_id = request.POST.get("message_id")
        title = request.POST.get("title")
        message = request.POST.get("message")
        message_type = request.POST.get("message_type")
        scheduled = request.POST.get("scheduled")
        scheduled_time = request.POST.get("scheduled_time") if scheduled else None

        UserMessage.objects.filter(id=message_id).update(
            title=title,
            message=message,
            message_type=message_type,
            scheduled=scheduled,
            scheduled_time=scheduled_time,
            created_by=request.user,
        )

        return redirect("notifications")
    return render(request, "notifications/edit_message.html")
