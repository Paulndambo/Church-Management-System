from django.urls import path

from apps.districts import views
from apps.districts.attendance.views import (
    DistrictAttendanceListView,
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
    # path("edit-district-meeting/", edit_district_meeting, name="edit-district-meeting"),
    path(
        "district-attendances/",
        DistrictAttendanceListView.as_view(),
        name="district-attendances",
    ),
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
    path(
        "district-finances/",
        views.DistrictFinanceListView.as_view(),
        name="district-finances",
    ),
    path(
        "district-sections/", views.SectionsListView.as_view(), name="district-sections"
    ),
    path("new-section/", views.new_section, name="new-section"),
    path("edit-section/", views.edit_section, name="edit-section"),
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
    path("capture-data/", views.capture_section_data, name="capture-data"),
    path("edit-section-data/", views.edit_section_data, name="edit-section-data"),
    path("delete-section-data/", views.delete_section_data, name="delete-section-data"),
    path("district-churches/", views.district_branches, name="district-churches"),
    path("new-district-church/", views.new_district_branch, name="new-district-church"),
]
