from django.urls import path

from apps.scheduling import views
from apps.scheduling.meetings import views as meeting_views
from apps.scheduling.appointments import views as appointment_views


urlpatterns = [
    path("new-member-request/", views.new_member_request, name="new-member-request"),
    path("edit-member-request/", views.edit_member_request, name="edit-member-request"),
    path("delete-member-request/", views.delete_member_request, name="delete-member-request"),

    path("prayer-requests/", views.PrayerRequestsListView.as_view(), name="prayer-requests"),
    path("baptism-requests/", views.BaptismRequestsListView.as_view(), name="baptism-requests"),
    path("burial-requests/", views.BurialRequestsListView.as_view(), name="burial-requests"),
    path("marriage-requests/", views.MarriageRequestsListView.as_view(), name="marriage-requests"),
 

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