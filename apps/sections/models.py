from django.db import models

from apps.core.models import AbstractBaseModel
# Create your models here.
class Section(AbstractBaseModel):
    name = models.CharField(max_length=255)
    presbyter = models.OneToOneField("users.User", on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey("districts.District", on_delete=models.CASCADE, related_name="districtsections")

    def __str__(self) -> str:
        return self.name