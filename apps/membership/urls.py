from django.urls import path

from apps.membership.views import (
    departments, new_department, edit_department, delete_department,
    branches, new_branch, edit_branch, delete_branch,
    MemberListView, new_member, edit_member, delete_member, branch_details,
    church_services, new_church_service, edit_church_service, delete_church_service
)

urlpatterns = [
    path("", MemberListView.as_view(), name="members"),
    path("new-member/", new_member, name="new-member"),
    path("edit-member/", edit_member, name="edit-member"),
    path("delete-member/", delete_member, name="delete-member"),
    
    path("departments/", departments, name="departments"),
    path("new-department/", new_department, name="new-department"),
    path("edit-department/", edit_department, name="edit-department"),
    path("delete-department/", delete_department, name="delete-department"),
    
    path("branches/", branches, name="branches"),
    path("branches/<int:id>/details/", branch_details, name="branch-detail"),
    path("new-branch/", new_branch, name="new-branch"),
    path("edit-branch/", edit_branch, name="edit-branch"),
    path("delete-branch/", delete_branch, name="delete-branch"),
    
    path("church-services/", church_services, name="church-services"),
    path("new-church-service/", new_church_service, name="new-church-service"),
    path("edit-church-service/", edit_church_service, name="edit-church-service"),
    path("delete-church-service/", delete_church_service, name="delete-church-service"),
]
