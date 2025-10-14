from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages



from apps.finances.models import MoneyAccount, MoneyAccountTransaction
from apps.core.models import UserActionLog
# Create your views here.
class MoneyAccountsListView(LoginRequiredMixin, ListView):
    model = MoneyAccount
    template_name = "money_accounts/money_accounts.html"
    context_object_name = "money_accounts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(account_name__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_types"] = ["Mpesa Account", "Bank Account", "Cash Account", "Expense Account"] 
        return context


@login_required
def money_account_details(request: HttpRequest, id: int):
    account = MoneyAccount.objects.get(id=id)
    account_transactions = MoneyAccountTransaction.objects.filter(
        Q(source__id=id) | Q(destination__id=id)
    )

    money_accounts = MoneyAccount.objects.all().exclude(id=id)

    context = {
        "account": account,
        "account_transactions": account_transactions,
        "money_accounts": money_accounts
    }
    return render(request, "money_accounts/money_account_details.html", context)


@login_required
@transaction.atomic
def new_money_account(request: HttpRequest):
    if request.method == "POST":
        account_name = request.POST.get("account_name")
        account_type = request.POST.get("account_type")
        balance = request.POST.get("balance")

        MoneyAccount.objects.create(
            account_name=account_name,
            account_type=account_type,
            balance=balance
        )
        return redirect("money-accounts")
    return render(request, "money-accounts/new_money_account.html")


@login_required
def edit_money_account(request: HttpRequest):
    if request.method == "POST":
        account_id = request.POST.get("account_id")
        account_name = request.POST.get("account_name")
        account_type = request.POST.get("account_type")
        

        MoneyAccount.objects.filter(id=account_id).update(
            account_name=account_name,
            account_type=account_type
        )

        return redirect("money-accounts")
    return render(request, "money-accounts/edit_money_account.html")


@login_required
@transaction.atomic
def transfer_money(request: HttpRequest):
    if request.method == "POST":
        try:
            source_id = request.POST.get("source_account")
            destination_id = request.POST.get("destination_account")
            amount = Decimal(request.POST.get("amount", "0").strip())
        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect("money-accounts")

        if source_id == destination_id:
            messages.error(request, "Source and destination accounts must be different.")
            return redirect("money-accounts")

        #source = get_object_or_404(MoneyAccount, id=source_id)
        #destination = get_object_or_404(MoneyAccount, id=destination_id)

        source = MoneyAccount.objects.select_for_update().get(id=source_id)
        destination = MoneyAccount.objects.select_for_update().get(id=destination_id)

        if source.balance < amount:
            messages.error(request, "Insufficient funds.")
            return redirect("money-account-detail", id=source_id)

        # Perform the transfer
        source.balance -= amount
        destination.balance += amount
        source.save()
        destination.save()

        # Record transactions
        MoneyAccountTransaction.objects.create(
            source=source,
            destination=destination,
            amount=amount,
            transaction_type="Debit",
            transferred_by=request.user
        )
        MoneyAccountTransaction.objects.create(
            source=destination,
            destination=source,
            amount=amount,
            transaction_type="Credit",
            transferred_by=request.user
        )

        UserActionLog.objects.create(
            user=request.user,
            action_type="Money Transfer",
            action_description=f"{request.user.username} has transferred {amount} from {source.account_name} to {destination.account_name}",
            metadata={
                "user_id": request.user.id,
                "username": request.user.username,
                "full_name": f"{request.user.first_name} {request.user.last_name}",
                "source_account": source.account_name,
                "destination_account": destination.account_name,
                "amount": float(amount)
            }
        )

        messages.success(request, f"Successfully transferred {amount} from {source.account_name} to {destination.account_name}.")
        return redirect("money-account-detail", id=source_id)

    return render(request, "money-accounts/transfer_money.html")


class MoneyAccountsTransactionsListView(LoginRequiredMixin, ListView):
    model = MoneyAccountTransaction
    template_name = "money_accounts/money_transactions.html"
    context_object_name = "transactions"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(account_type__icontains=search_query)
            )
        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_types"] = ["Mpesa Account", "Bank Account", "Cash Account"] 
        return context