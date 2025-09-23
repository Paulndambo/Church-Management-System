from django.db import models
from decimal import Decimal
import calendar
from django.utils.timezone import now as date_today


from apps.core.models import AbstractBaseModel
# Create your models here.
class DepartmentSaving(AbstractBaseModel):
    department = models.ForeignKey("membership.Department", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    savings_date = models.DateField()
    branch = models.ForeignKey("membership.Branch", on_delete=models.SET_NULL, null=True)
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    

class MemberDepartmentSaving(AbstractBaseModel):
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    savings_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.member.user.username if self.member else "Member"
        

class MemberTithing(AbstractBaseModel):
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    tithing_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.member.user.username if self.member else "Tithe"
    
    
class Offering(AbstractBaseModel):
    branch = models.ForeignKey("membership.Branch", on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey("attendances.ChurchService", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    offering_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
        

class MemberOffering(AbstractBaseModel):
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey("membership.Branch", on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey("attendances.ChurchService", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    offering_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
        

class ChurchExpense(AbstractBaseModel):
    name = models.CharField(max_length=255)
    amount_allocated = models.DecimalField(max_digits=100, decimal_places=2)
    date_spend = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name
    


class ChurchDonation(AbstractBaseModel):
    donor = models.CharField(max_length=255, null=True, blank=True)
    purpose = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    donation_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    receipt_number = models.CharField(max_length=255, null=True, blank=True)


class ChurchLedger(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    direction = models.CharField(max_length=50, choices=(("Income", "Income"), ("Expense", "Expense")))
    month = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=Decimal('0'))
    
    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs) -> None:
        if not self.month:
            self.month = calendar.month_name[date_today().month]
        if not self.year:
            self.year = date_today().year

        last_entry = ChurchLedger.objects.order_by('-created_at').first()
        if last_entry:
            self.balance = last_entry.balance + self.amount
        elif not last_entry:
            self.balance = self.amount
        return super().save(*args, **kwargs)