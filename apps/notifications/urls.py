from django.urls import path
from apps.notifications import views

urlpatterns = [
    path("", views.UserMessageListView.as_view(), name="notifications"),
    path("create-message/", views.create_user_message, name="create-message"),
    path("edit-message/", views.edit_user_message, name="edit-message"),
]
