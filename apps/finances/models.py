from django.db import models
from decimal import Decimal

from apps.core.models import AbstractBaseModel
# Create your models here.
class MoneyAccount(AbstractBaseModel):
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=Decimal('0'))
    is_expense_account = models.BooleanField(default=False)

    def __str__(self):
        return self.account_name


class MoneyAccountTransaction(AbstractBaseModel):
    source = models.ForeignKey(MoneyAccount, on_delete=models.CASCADE, related_name="sourceaccounts", null=True)
    destination = models.ForeignKey(MoneyAccount, on_delete=models.CASCADE, related_name="destinationaccounts", null=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, default=Decimal('0'))
    transferred_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=255, null=True, choices=(("Credit", "Credit"), ("Debit", "Debit")))
