from django.db import models

from apps.core.models import AbstractBaseModel
# Create your models here.
POSITION_CHOICES = (
    ("Church Member", "Church Member"),
    ("Pastor", "Pastor"),
    ("Men Department Leader", "Men Department Leader"),
    ("Women Department Leader", "Women Department Leader"),
    ("Teens Department Leader", "Teens Department Leader"),
    ("Church Secretary", "Church Secretary"),
    ("Church Treasurer", "Church Treasurer"),
)

STATUS_CHOICES = (
    ("Active", "Active"),
    ("Inactive", "Inactive"),
    ("Suspended", "Suspended"),
)

class Department(AbstractBaseModel):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class Branch(AbstractBaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=500, null=True)
    town = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    def branch_members(self):
        return self.branchmembers.count()


class Member(AbstractBaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name="branchmembers")
    position = models.CharField(max_length=255, choices=POSITION_CHOICES, default="Church Member")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Active")
    member_since = models.DateField(null=True)
    
    def __str__(self):
        return self.user.username
    
    def name(self):
        return self.user.get_full_name()


class ChurchService(AbstractBaseModel):
    name = models.CharField(max_length=255)
    service_day = models.CharField(max_length=255, default="Sunday")
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    
    def __str__(self):
        return self.name