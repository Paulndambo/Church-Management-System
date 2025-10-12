from django.urls import path

from apps.projects import views

urlpatterns = [
    path("", views.ProjectsListView.as_view(), name="projects"),
    path("<int:id>/details/", views.project_details, name="project-detail"),
    path("new-project/", views.new_project, name="new-project"),
    path("edit-project/", views.edit_project, name="edit-project"),
    path(
        "contributions/",
        views.ProjectContributionsListView.as_view(),
        name="contributions",
    ),
    path("pledges/", views.ProjectPledgesListView.as_view(), name="pledges"),
    path("new-pledge/", views.new_pledge, name="new-pledge"),
    path("edit-pledge/", views.edit_pledge, name="edit-pledge"),
    path("redeem-pledge/", views.redeem_pledge, name="redeem-pledge"),
]
