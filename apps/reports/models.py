from django.db import models

from apps.core.models import AbstractBaseModel


# Create your models here.
class ChurchMonthlyReport(AbstractBaseModel):
    branch = models.ForeignKey(
        "membership.Branch",
        on_delete=models.CASCADE,
        related_name="branchmonthlyreports",
    )
    month_name = models.CharField(max_length=255)
    month_number = models.IntegerField()
    year = models.IntegerField(default=2025)

    def __str__(self) -> str:
        return self.month_name
