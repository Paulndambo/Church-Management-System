from django.urls import path

from apps.sections import views

urlpatterns = [
    path("", views.SectionsListView.as_view(), name="sections"),
    path("<int:id>/", views.section_details, name="section-detail"),
    path("new-section/", views.new_section, name="new-section"),
    path("edit-section/", views.edit_section, name="edit-section"),

    path("new-section-church/", views.new_branch, name="new-section-church"),
    path("edit-section-church/", views.edit_branch, name="edit-section-church"),
    path("branch-details/<int:id>/", views.branch_details, name="branch-detail"),

    path("capture-church-data/", views.capture_church_data, name="capture-church-data"),
    path("edit-section-data/", views.edit_section_data, name="edit-section-data"),
]