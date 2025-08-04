from django.db import models
from decimal import Decimal

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
        return self.member.user.username
        

class MemberTithing(AbstractBaseModel):
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    tithing_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.member.user.username
    
    
class Offering(AbstractBaseModel):
    branch = models.ForeignKey("membership.Branch", on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey("membership.ChurchService", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    offering_date = models.DateField()
    captured_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
        

class MemberOffering(AbstractBaseModel):
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey("membership.Branch", on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey("membership.ChurchService", on_delete=models.SET_NULL, null=True)
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