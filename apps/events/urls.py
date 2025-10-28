from django.urls import path
from apps.events import views

urlpatterns = [
    path("", views.ChurchEventListView.as_view(), name="events"),
    path("<int:id>/details/", views.event_details, name="event-detail"),
    path("new-event/", views.new_church_event, name="new-event"),
    path("edit-event/", views.edit_church_event, name="edit-event"),

    path("new-event-ticket/", views.create_member_event_ticket, name="new-event-ticket"),
    path("new-event-ticket-type/", views.create_event_ticket_type, name="new-event-ticket-type"),
    path("edit-event-ticket-type/", views.edit_event_ticket_type, name="edit-event-ticket-type"),
    path("<int:id>/event-tickets/", views.EventTicketsListView.as_view(), name="event-tickets"),
]