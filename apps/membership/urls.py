from django.urls import path

from apps.membership import views

urlpatterns = [
    path("", views.MemberListView.as_view(), name="members"),
    path("new-member/", views.new_member, name="new-member"),
    path("edit-member/", views.edit_member, name="edit-member"),
    path("delete-member/", views.delete_member, name="delete-member"),
    
    path("departments/", views.departments, name="departments"),
    path("new-department/", views.new_department, name="new-department"),
    path("edit-department/", views.edit_department, name="edit-department"),
    path("delete-department/", views.delete_department, name="delete-department"),
    
    path("branches/", views.branches, name="branches"),
    path("branches/<int:id>/details/", views.branch_details, name="branch-detail"),
    path("new-branch/", views.new_branch, name="new-branch"),
    path("edit-branch/", views.edit_branch, name="edit-branch"),
    path("delete-branch/", views.delete_branch, name="delete-branch"),
    
    path("church-services/", views.church_services, name="church-services"),
    path("new-church-service/", views.new_church_service, name="new-church-service"),
    path("edit-church-service/", views.edit_church_service, name="edit-church-service"),
    path("delete-church-service/", views.delete_church_service, name="delete-church-service"),

    path("attendances/", views.ServiceAttendaceView.as_view(), name="attendances"),
    path("new-attendance/", views.new_attendance, name="new-attendance"),
]
