from django.urls import path

from apps.finances.views import (
    MoneyAccountsListView,
    MoneyAccountsTransactionsListView,
    new_money_account,
    edit_money_account,
    money_account_details,
    transfer_money
)

urlpatterns = [
    path("money-accounts", MoneyAccountsListView.as_view(), name="money-accounts"),
    path("<int:id>/details/", money_account_details, name="money-account-detail"),
    path("new-money-account/", new_money_account, name="new-money-account"),
    path("edit-money-account/", edit_money_account, name="edit-money-account"),
    path("money-accounts-transactions/", MoneyAccountsTransactionsListView.as_view(), name="money-accounts-transactions"),
    path("transfer-money/", transfer_money, name="transfer-money"),
]