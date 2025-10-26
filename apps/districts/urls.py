from django.urls import path

from apps.districts import views
from apps.districts.attendance.views import (
    DistrictMeetingListView,
    new_district_meeting,
    DistrictMeetingAttendanceListView,
    mark_district_meeting_attendance,
    district_meeting_details,
    create_meeting_attendant,
    edit_meeting_attendant,
)

from apps.districts.reports.views import district_home

urlpatterns = [
    path("", district_home, name="district-home"),
    path(
        "district-meetings/",
        DistrictMeetingListView.as_view(),
        name="district-meetings",
    ),
    path(
        "district-meetings/<int:id>/",
        district_meeting_details,
        name="district-meeting-details",
    ),
    path("new-district-meeting/", new_district_meeting, name="new-district-meeting"),
    path("create-attendant/", create_meeting_attendant, name="create-attendant"),
    path("edit-attendant/", edit_meeting_attendant, name="edit-attendant"),
    path(
        "district-meeting-attendances/",
        DistrictMeetingAttendanceListView.as_view(),
        name="district-meeting-attendances",
    ),
    path(
        "mark-district-meeting-attendance/<int:id>/",
        mark_district_meeting_attendance,
        name="mark-district-meeting-attendance",
    ),
 
    path("presbyters/", views.PresbytersListView.as_view(), name="presbyters"),
    path("new-presbyter/", views.new_presbyter, name="new-presbyter"),
    path("edit-presbyter/", views.edit_presbyter, name="edit-presbyter"),
    path(
        "district-reports/",
        views.DistrictReportListView.as_view(),
        name="district-reports",
    ),
    path(
        "district-reports/<int:id>/details/",
        views.district_report_details,
        name="district-report-details",
    ),
    path("new-report/", views.new_report, name="new-report"),
    path("edit-report/", views.edit_report, name="edit-report"),
    path(
        "district-expenses/",
        views.DistrictExpenseListView.as_view(),
        name="district-expenses",
    ),
    path("new-district-expense/", views.new_expense, name="new-district-expense"),
    path("edit-district-expense/", views.edit_expense, name="edit-district-expense"),
    
    path("district-churches/", views.DistrictBranchesListView.as_view(), name="district-churches"),
    path("new-district-church/", views.new_district_branch, name="new-district-church"),
    path("edit-district-church/", views.edit_district_branch, name="edit-district-church"),
    path("delete-district-church/", views.delete_district_branch, name="delete-district-church"),
]
