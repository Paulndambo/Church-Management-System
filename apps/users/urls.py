from django.urls import path
from apps.users.views import (
    login_user,
    logout_user,
    VisitorListView,
    new_visitor,
    edit_visitor,
    delete_visitor,
    checkin_visitor
)

urlpatterns = [
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("visitors/", VisitorListView.as_view(), name="visitors"),
    path("new-visitor/", new_visitor, name="new-visitor"),
    path("edit-visitor/", edit_visitor, name="edit-visitor"),
    path("delete-visitor/", delete_visitor, name="delete-visitor"),
    path("checkin-visitor/", checkin_visitor, name="checkin-visitor"),
]
