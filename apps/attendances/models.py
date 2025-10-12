from django.db import models
from apps.core.models import AbstractBaseModel
import calendar
from datetime import datetime

date_today = datetime.now().date()

# Create your models here.
class ChurchService(AbstractBaseModel):
    name = models.CharField(max_length=255)
    service_day = models.CharField(max_length=255, default="Sunday")
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    status = models.CharField(
        max_length=50,
        choices=(("Active", "Active"), ("Inactive", "Inactive")),
        default="Active",
    )

    def __str__(self):
        return self.name


class ServiceAttendance(AbstractBaseModel):
    member = models.ForeignKey("membership.Member", on_delete=models.CASCADE)
    service = models.ForeignKey(ChurchService, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=(("Present", "Present"), ("Absent", "Absent")),
        default="Present",
    )
    month = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)

    def __str__(self):
        return (
            f"{self.member.user.get_full_name()} - {self.service.name} on {date_today}"
        )




class ServiceAttendanceMetric(AbstractBaseModel):
    branch = models.ForeignKey("membership.Branch", on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(ChurchService, on_delete=models.CASCADE)
    month = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)
    total_present = models.IntegerField(default=0)
    service_date = models.DateField()
    gender = models.CharField(
        max_length=20,
        choices=(("Male", "Male"), ("Female", "Female"), ("Both", "Both")),
        default="Both",
    )
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name="attendancerecorders")

    def __str__(self):
        return f"{self.service.name} - {self.month} {self.year}"
