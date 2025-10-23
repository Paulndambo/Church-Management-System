from django.db import models
from apps.core.models import AbstractBaseModel


# Create your models here.
class Section(AbstractBaseModel):
    name = models.CharField(max_length=255)
    presbyter = models.OneToOneField("users.User", on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(
        "districts.District", on_delete=models.CASCADE, related_name="districtsections"
    )
    has_presbyter = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class SectionReport(AbstractBaseModel):
    report = models.ForeignKey("districts.DistrictReport", on_delete=models.CASCADE, null=True)
    district = models.ForeignKey("districts.District", on_delete=models.CASCADE, related_name="districtsectionreports")
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    month=models.CharField(max_length=255, null=True)
    year=models.IntegerField(null=True)
    

    def __str__(self) -> str:
        return self.district.name
