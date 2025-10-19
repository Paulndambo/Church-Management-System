from django.urls import path

from apps.scheduling import views

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
]