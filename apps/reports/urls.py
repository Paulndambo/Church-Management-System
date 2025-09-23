from django.urls import path
from apps.reports import views
from apps.districts.views import district_report

urlpatterns = [
    path("", views.MonthlyReportView.as_view(), name="monthly-reports"),
    path("<int:report_id>/", views.MonthlyReportView.as_view(), name="monthly-reports"),
    path("new-monthly-report/", views.new_monthly_report, name="new-monthly-report"),
    path("edit-monthly-report/", views.edit_monthly_report, name="edit-monthly-report"),
    path("district-report/<int:id>/", district_report, name="district-report"), 
]