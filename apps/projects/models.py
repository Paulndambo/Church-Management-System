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
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, related_name="memberprojectpledges")
    partner = models.ForeignKey("partners.ChurchPartner", on_delete=models.SET_NULL, null=True, related_name="partnerprojectpledges")
    amount_pledged = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    amount_redeemed = models.DecimalField(max_digits=255, decimal_places=2, default=Decimal('0'))
    full_redeemed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.project.name   
    
    def balance(self):
        return self.amount_pledged - self.amount_redeemed
    
    def pledger(self):
        if self.member:
            return self.member.user.get_full_name()
        elif self.partner:
            return self.partner.name
        return "N/A"
    
class ProjectContribution(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey("membership.Member", on_delete=models.SET_NULL, null=True, related_name="memberprojectcontributions")
    partner = models.ForeignKey("partners.ChurchPartner", on_delete=models.SET_NULL, null=True, related_name="partnerprojectcontributions")
    pledge = models.ForeignKey(ProjectPledge, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    
    def __str__(self):
        return self.project.name
    
    def contributor(self):
        if self.member:
            return self.member.user.get_full_name()
        elif self.partner:
            return self.partner.name
        return "N/A"