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
    path("groups/", views.MemberGroupsListView.as_view(), name="groups"),
    path("new-group/", views.new_member_group, name="new-group"),
    path("edit-group/", views.edit_member_group, name="edit-group"),
    path("delete-group/", views.delete_member_group, name="delete-group"),
    path("group/<int:id>/details/", views.group_details, name="group-detail"),
    path("new-group-member/", views.add_group_member, name="new-group-member"),
    path("edit-group-member/", views.edit_group_member, name="edit-group-member"),
]
