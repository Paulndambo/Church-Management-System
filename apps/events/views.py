from decimal import Decimal
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q
from typing import Any
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from apps.membership.models import Department, Branch, Member, MemberGroup, GroupMember
from apps.core.models import UserActionLog
from apps.users.models import User

from apps.events.models import (
    ChurchEvent, ChurchEventTicketType, ChurchEventTicket, EventAttendance
)

from apps.events.ticket_number_generator import generate_ticket_number
# Create your views here.
class ChurchEventListView(LoginRequiredMixin, ListView):
    model = ChurchEvent
    template_name = "events/events.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs: dict[str, Any]):
        context = super().get_context_data(**kwargs)
        context["event_types"] = ["Paid Event", "Free Event"]
        return context
    


@login_required
@transaction.atomic
def new_church_event(request: HttpRequest):
    if request.method == "POST":
        name = request.POST.get("name")
        event_type = request.POST.get("event_type")
        starts_on = request.POST.get("starts_on")
        ends_on = request.POST.get("ends_on")
     

        event = ChurchEvent.objects.create(
            name=name,
            event_type=event_type,
            starts_on=starts_on,
            ends_on=ends_on
        )

        if event.event_type == "Free Event":
            ChurchEventTicketType.objects.create(
                event=event,
                title="Free Ticket",
                cost=0,
                total_tickets=1000
            )


        return redirect("events")
    return render(request, "events/new_event.html")


@login_required
@transaction.atomic
def edit_church_event(request: HttpRequest):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        name = request.POST.get("name")
        description = request.POST.get("description")
        event_type = request.POST.get("event_type")
        starts_on = request.POST.get("starts_on")
        ends_on = request.POST.get("ends_on")
     

        ChurchEvent.objects.filter(id=event_id).update(
            name=name,
            description=description,
            event_type=event_type,
            starts_on=starts_on,
            ends_on=ends_on
        )

        if event_type == "Free Event":
            ticket = ChurchEventTicketType.objects.filter(event__id=event_id).first()
            if ticket:
                print("Event free ticket already exists")
            else:
                ChurchEventTicketType.objects.create(
                    event_id=event_id,
                    title="Free Ticket",
                    cost=0,
                    total_tickets=1000
                )

        return redirect("events")
    return render(request, "events/edit_event.html")


@login_required
def event_details(request: HttpRequest, id: int):
    event = ChurchEvent.objects.get(id=id)
    ticket_types = event.eventtickettypes.all()
    event_attendances = event.eventattendances.all()
    total_tickets = sum(event.eventtickets.all().values_list("number_of_tickets", flat=True))
    total_amount_raised = sum(event.eventtickets.all().values_list("total_amount", flat=True))


    context = {
        "event": event,
        "ticket_types": ticket_types,
        "tickets_sold": total_tickets,
        "total_attendance": event_attendances.count(),
        "total_amount": total_amount_raised,
        "members": Member.objects.all()
    }
    return render(request, "events/event_details.html", context)


@login_required
@transaction.atomic
def create_member_event_ticket(request: HttpRequest):
    if request.method == "POST":
        event = request.POST.get("event")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        ticket_type = request.POST.get("ticket_type")
        number_of_tickets = request.POST.get("number_of_tickets")
        amount_paid = request.POST.get("amount_paid")

        event_ticket_type = ChurchEventTicketType.objects.get(id=ticket_type)
        church_event = ChurchEvent.objects.get(id=event)

        ticket_number = generate_ticket_number(
            event=church_event,
            ticket_type=event_ticket_type,
            last_ticket=ChurchEventTicket.objects.order_by("-created_at").first()
        )

        ticket = ChurchEventTicket.objects.create(
            ticket_number=ticket_number,
            event_id=event,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            number_of_tickets=number_of_tickets,
            ticket_type_id=ticket_type,
            amount_paid=amount_paid
        )

        ticket.total_amount = Decimal(number_of_tickets) * Decimal(event_ticket_type.cost)
        ticket.save()

        ticket.ticket_type.purchased += int(number_of_tickets)
        ticket.ticket_type.total_tickets -= int(number_of_tickets)
        ticket.ticket_type.save()

        return redirect("event-detail", id=event)
    return render(request, "events/new_event_ticket.html")


@login_required
@transaction.atomic
def create_event_ticket_type(request: HttpRequest):
    if request.method == "POST":
        event = request.POST.get("event")
        title = request.POST.get("title")
        cost = request.POST.get("cost")
        total_tickets = request.POST.get("total_tickets")

      
        ChurchEventTicketType.objects.create(
            event_id=event,
            title=title,
            cost=cost,
            total_tickets=total_tickets
        )
        return redirect("event-detail", id=event)
    return render(request, "events/new_ticket_type.html")


@login_required
@transaction.atomic
def edit_event_ticket_type(request: HttpRequest):
    if request.method == "POST":
        ticket_type_id = request.POST.get("ticket_type_id")
        event = request.POST.get("event_id")
        title = request.POST.get("title")
        cost = request.POST.get("cost")
        total_tickets = request.POST.get("total_tickets")

      
        ChurchEventTicketType.objects.filter(id=ticket_type_id).update(
            event_id=event,
            title=title,
            cost=cost,
            total_tickets=total_tickets
        )
        return redirect("event-detail", id=event)
    return render(request, "events/edit_ticket_type.html")