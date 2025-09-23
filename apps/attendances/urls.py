from django.urls import path

from apps.attendances import views

urlpatterns = [
    
    path("service-attendances/", views.ServiceAttendanceMetricsListView.as_view(), name="service-attendances"),
    path("record-service-attendance/", views.record_service_attendance, name="record-service-attendance"),
    ### Church Services Management
    path("church-services/", views.church_services, name="church-services"),
    path("new-church-service/", views.new_church_service, name="new-church-service"),
    path("edit-church-service/", views.edit_church_service, name="edit-church-service"),
    path("delete-church-service/", views.delete_church_service, name="delete-church-service"),

    path("member-attendances/", views.ServiceAttendaceView.as_view(), name="member-attendances"),
    path("new-attendance/", views.new_attendance, name="new-attendance"),
]