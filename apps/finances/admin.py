from django.contrib import admin

from apps.finances.models import MoneyAccount, MoneyAccountTransaction
# Register your models here.
@admin.register(MoneyAccountTransaction)
class MoneyAccountTransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "source", "destination", "transaction_type", "amount", "created_at"]


@admin.register(MoneyAccount)
class MoneyAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "account_name", "account_type", "balance", "created_at"]
