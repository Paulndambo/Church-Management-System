from django.urls import path

from apps.partners import views

urlpatterns = [
    path("", views.PartnersListView.as_view(), name="partners"),
    path("new-partner/", views.new_partner, name="new-partner"),
    path("edit-partner/", views.edit_partner, name="edit-partner"),
    path("delete-partner/", views.delete_partner, name="delete-partner"),
]
