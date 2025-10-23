from django.db import models
from decimal import Decimal

from apps.core.models import AbstractBaseModel


# Create your models here.
class District(AbstractBaseModel):
    church = models.ForeignKey("core.Church", on_delete=models.SET_NULL, null=True, related_name="churchdistricts")
    name = models.CharField(max_length=255)
    supretendent = models.OneToOneField("users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


class DistrictReport(AbstractBaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="reports")
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)


class DistrictExpense(AbstractBaseModel):
    report = models.ForeignKey(DistrictReport, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtexpenses")
    expense_name = models.CharField(max_length=255)
    amount_spend = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.expense_name


class DistrictMeeting(AbstractBaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    meeting_date = models.DateField()
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.district.name


class DistrictMeetingAttendace(AbstractBaseModel):
    meeting = models.ForeignKey(DistrictMeeting, on_delete=models.CASCADE, related_name="districtmeetingattendances")
    full_name = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    role = models.CharField(max_length=255, null=True)
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.full_name if self.full_name else ""
    

class KAGDistrictMonthlyReport(AbstractBaseModel):
    report = models.ForeignKey("districts.DistrictReport", on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtmonthlychurchreports")
    section = models.ForeignKey("sections.Section", on_delete=models.SET_NULL, null=True, related_name="sectionmonthlychurchreports")
    church = models.ForeignKey("membership.Branch", on_delete=models.SET_NULL, null=True, related_name="churchmonthlyreports")
    section_report = models.ForeignKey("sections.SectionReport", on_delete=models.SET_NULL, null=True)
    general_fund = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    sunday_school = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    pastors_tithe = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    presbyter_tithe = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    easter = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    special_offering = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    kenya_kids = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    pastors_fund = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    kagdom = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    district_missions = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    resource_mobilisation = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    church_support = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    church_welfare = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    children = models.IntegerField(default=0)
    adult = models.IntegerField(default=0)
    total_collected = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    pastor = models.ForeignKey("users.Pastor", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.district.name

    def total_amount(self):
        return (
            self.general_fund
            + self.sunday_school
            + self.pastors_fund
            + self.pastors_tithe
            + self.presbyter_tithe
            + self.easter
            + self.special_offering
            + self.kenya_kids
        )

    def non_tithe_totals(self):
        return self.easter + self.special_offering + self.kenya_kids

    def tithe_totals(self):
        return self.pastors_tithe + self.presbyter_tithe

    def revenue_total(self):
        return self.general_fund + self.sunday_school + self.pastors_fund