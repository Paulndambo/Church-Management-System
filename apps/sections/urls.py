from django.urls import path

from apps.sections import views
from apps.sections.pastors import views as pastors_views
from apps.sections.reports import views as reports_views

urlpatterns = [
    path("", views.SectionsListView.as_view(), name="sections"),
    path("<int:id>/details/", views.section_details, name="section-detail"),
    path("new-section/", views.new_section, name="new-section"),
    path("edit-section/", views.edit_section, name="edit-section"),

    path("branch-details/<int:id>/", views.branch_details, name="branch-detail"),

    path("capture-church-data/", views.capture_church_data, name="capture-church-data"),
    path("edit-church-data/", views.edit_section_data, name="edit-church-data"),
    path("delete-church-data/", views.delete_church_data, name="delete-church-data"),

    path("district-pastors/", pastors_views.PastorsListView.as_view(), name="district-pastors"),
    path("new-pastor/", pastors_views.new_pastor, name="new-pastor"),
    path("edit-pastor/", pastors_views.edit_pastor, name="edit-pastor"),
    path("delete-pastor/", pastors_views.delete_pastor, name="delete-pastor"),

    path("district-pastor-associates/", pastors_views.PastorsAssociatesListView.as_view(), name="district-pastor-associates"),
    path("new-pastor-associate/", pastors_views.new_pastor_associate, name="new-pastor-associate"),
    path("edit-pastor-associate/", pastors_views.edit_pastor_associate, name="edit-pastor-associate"),

    path("section-reports/", reports_views.SectionReportsListView.as_view(), name="section-reports"),
    path("new-section-reports/", reports_views.new_section_reports, name="new-section-reports"),
    path("section-reports/<int:id>/details/", reports_views.section_report_details, name="section-report-detail"),
    path("monthly-report/<int:id>/details/", reports_views.MonthReportDetailView.as_view(), name="monthly-report-detail"),
]