from django.urls import path

from apps.sections import views

urlpatterns = [
    path("", views.SectionsListView.as_view(), name="sections"),
    path("<int:id>/", views.section_details, name="section-detail"),
    path("new-section/", views.new_section, name="new-section"),
    path("edit-section/", views.edit_section, name="edit-section"),

    path("branch-details/<int:id>/", views.branch_details, name="branch-detail"),

    path("capture-church-data/", views.capture_church_data, name="capture-church-data"),
    path("edit-church-data/", views.edit_section_data, name="edit-church-data"),

    path("district-pastors/", views.PastorsListView.as_view(), name="district-pastors"),
    path("new-pastor/", views.new_pastor, name="new-pastor"),
    path("edit-pastor/", views.edit_pastor, name="edit-pastor"),
]