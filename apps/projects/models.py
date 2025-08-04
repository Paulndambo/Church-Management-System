from django.db import models
from decimal import Decimal

from apps.core.models import AbstractBaseModel
# Create your models here.
class Project(AbstractBaseModel):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    total_budget = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    amount_raised = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
    def status(self):
        return "Completed" if self.completed else "Pending"
    
 
class ProjectPledge(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    amount_pledged = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    amount_redeemed = models.DecimalField(max_digits=255, decimal_places=2, default=Decimal('0'))
    
    def __str__(self):
        return self.project.name   
    
    def balance(self):
        return self.amount_pledged - self.amount_redeemed
     
    
class ProjectContribution(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True)
    pledge = models.ForeignKey(ProjectPledge, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    
    def __str__(self):
        return self.project.name