from django.urls import path

from apps.scheduling import views
from apps.scheduling.meetings import views as meeting_views
from apps.scheduling.appointments import views as appointment_views


urlpatterns = [
    path("prayer-requests/", views.PrayerRequestsListView.as_view(), name="prayer-requests"),
    path("new-prayer-request/", views.new_prayer_request, name="new-prayer-request"),
    path("edit-prayer-request/", views.edit_prayer_request, name="edit-prayer-request"),
    path("delete-prayer-request/", views.delete_prayer_request, name="delete-prayer-request"),


    path("baptism-requests/", views.BaptismRequestsListView.as_view(), name="baptism-requests"),
    path("new-baptism-request/", views.new_baptism_request, name="new-baptism-request"),
    path("edit-baptism-request/", views.edit_baptism_request, name="edit-baptism-request"),
    path("delete-baptism-request/", views.delete_baptism_request, name="delete-baptism-request"),


    path("burial-requests/", views.BurialRequestsListView.as_view(), name="burial-requests"),
    path("new-burial-request/", views.new_burial_request, name="new-burial-request"),
    path("edit-burial-request/", views.edit_burial_request, name="edit-burial-request"),
    path("delete-burial-request/", views.delete_burial_request, name="delete-burial-request"),

    path("marriage-requests/", views.MarriageRequestsListView.as_view(), name="marriage-requests"),
    path("new-marriage-request/", views.new_marriage_request, name="new-marriage-request"),
    path("edit-marriage-request/", views.edit_marriage_request, name="edit-marriage-request"),
    path("delete-marriage-request/", views.delete_marriage_request, name="delete-marriage-request"),

    path("church-meetings/", meeting_views.ChurchMeetingsListView.as_view(), name="church-meetings"),
    path("church-meeting/<int:id>/details/", meeting_views.church_meeting_detail, name="church-meeting-detail"),
    path("new-church-meeting/", meeting_views.new_church_meeting, name="new-church-meeting"),
    path("edit-church-meeting/", meeting_views.edit_church_meeting, name="edit-church-meeting"),
    path("delete-church-meeting/", meeting_views.delete_church_meeting, name="delete-church-meeting"),
    path("add-church-meeting-attendance/", meeting_views.add_church_meeting_attendance, name="add-church-meeting-attendance"),
    path("edit-church-meeting-attendance/", meeting_views.edit_church_meeting_attendance, name="edit-church-meeting-attendance"),
    path("delete-church-meeting-attendance/", meeting_views.delete_church_meeting_attendance, name="delete-church-meeting-attendance"),

    path("appointments/", appointment_views.AppointmentsListView.as_view(), name="appointments"),
    path("new-appointment/", appointment_views.new_appointment, name="new-appointment"),
    path("edit-appointment/", appointment_views.edit_appointment, name="edit-appointment"),
    path("mark-appointment/", appointment_views.approve_or_decline, name="mark-appointment"),
]