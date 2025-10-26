from django.urls import path

from apps.payments import views
from apps.payments.offerings import views as offering_views


urlpatterns = [
    path("offerings/", offering_views.OfferingsListView.as_view(), name="offerings"),
    path("new-offering/", offering_views.new_offering, name="new-offering"),
    path("tithings/", views.MemberTithingsListView.as_view(), name="tithings"),
    path("new-tithing/", views.new_member_tithing, name="new-tithing"),
    path(
        "department-savings/",
        views.DepartmentSavingsListView.as_view(),
        name="department-savings",
    ),
    path("new-savings/", views.new_department_saving, name="new-savings"),
    path("expenses/", views.ChurchExpensesListView.as_view(), name="expenses"),
    path("new-expense/", views.new_expense, name="new-expense"),
    path("church-ledger/", views.ChurchLedgerListView.as_view(), name="church-ledger"),
    path("donations/", views.ChurchDonationsListView.as_view(), name="donations"),
    path("new-donation/", views.new_church_donation, name="new-donation"),
]
