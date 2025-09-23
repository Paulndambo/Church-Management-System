from django.db import models

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
    
    
class DistrictAttendance(AbstractBaseModel):
    report = models.ForeignKey(DistrictReport, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtattendance")
    section = models.ForeignKey("sections.Section", on_delete=models.SET_NULL, null=True)
    children = models.IntegerField(default=0)
    adult = models.IntegerField(default=0)
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.district.name    

    def total_attendance(self):
        return self.adult + self.children    


class DistrictFinance(AbstractBaseModel):
    report = models.ForeignKey(DistrictReport, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtfinances")
    section = models.ForeignKey("sections.Section", on_delete=models.SET_NULL, null=True)
    general_fund = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    sunday_school = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    pastors_tithe = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    presbyter_tithe = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    easter = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    special_offering = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    kenya_kids = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    pastors_fund = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    kagdom = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    district_missions = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    resource_mobilisation = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    church_support = models.DecimalField(max_digits=100, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.district.name    
    
    def total_amount(self):
        return self.general_fund + self.sunday_school + self.pastors_fund + self.pastors_tithe + self.presbyter_tithe + self.easter + self.special_offering + self.kenya_kids
    
    def non_tithe_totals(self):
        return self.easter + self.special_offering + self.kenya_kids
    
    def tithe_totals(self):
        return self.pastors_tithe + self.presbyter_tithe
    
    def revenue_total(self):
        return self.general_fund + self.sunday_school + self.pastors_fund
    

class SectionReport(AbstractBaseModel):
    report = models.ForeignKey(DistrictReport, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtsectionreports")
    section = models.ForeignKey("sections.Section", on_delete=models.SET_NULL, null=True)
    general_fund = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    sunday_school = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    pastors_tithe = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    presbyter_tithe = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    easter = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    special_offering = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    kenya_kids = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    pastors_fund = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    kagdom = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    district_missions = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    resource_mobilisation = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    church_support = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    church_welfare = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    children = models.IntegerField(default=0)
    adult = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.district.name    
    
    def total_amount(self):
        return self.general_fund + self.sunday_school + self.pastors_fund + self.pastors_tithe + self.presbyter_tithe + self.easter + self.special_offering + self.kenya_kids
    
    def non_tithe_totals(self):
        return self.easter + self.special_offering + self.kenya_kids
    
    def tithe_totals(self):
        return self.pastors_tithe + self.presbyter_tithe
    
    def revenue_total(self):
        return self.general_fund + self.sunday_school + self.pastors_fund
    
    
class DistrictExpense(AbstractBaseModel):
    report = models.ForeignKey(DistrictReport, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districtexpenses")
    expense_name = models.CharField(max_length=255)
    amount_spend = models.DecimalField(max_digits=100, decimal_places=2, default=0)
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
    section = models.ForeignKey("sections.Section", on_delete=models.CASCADE)
    presbyter = models.ForeignKey("users.User", on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    month = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    
    def __str__(self) -> str:
        return self.presbyter.get_full_name()
    
    def status(self):
        return "Present" if self.present else "Absent"