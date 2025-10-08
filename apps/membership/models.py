import calendar
from django.db import models
from django.utils.timezone import now as date_today
from apps.core.models import AbstractBaseModel
from apps.users.models import Pastor

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
    church = models.ForeignKey("core.Church", on_delete=models.SET_NULL, null=True, name="churchbranches")
    section = models.ForeignKey("sections.Section", on_delete=models.SET_NULL, null=True, related_name="sectionbranches")
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=500, null=True)
    town = models.CharField(max_length=255)
    pastor = models.OneToOneField("users.User", on_delete=models.SET_NULL, null=True, related_name="branchpastor")

    def __str__(self):
        return self.name

    def branch_members(self):
        return self.branchmembers.count()
    
    def pastor(self):
        return Pastor.objects.filter(church=self).first()


class Member(AbstractBaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, related_name="branchmembers"
    )
    position = models.CharField(
        max_length=255, choices=POSITION_CHOICES, default="Church Member"
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Active")
    member_since = models.DateField(null=True)

    def __str__(self):
        return self.user.username

    def name(self):
        return self.user.get_full_name()


class MemberGroup(AbstractBaseModel):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    date_started = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=(("Active", "Active"), ("Inactive", "Inactive")),
        default="Active",
    )

    def __str__(self):
        return self.name

    def members_count(self):
        return self.groupmembers.count()


class GroupMember(AbstractBaseModel):
    group = models.ForeignKey(MemberGroup, on_delete=models.CASCADE, related_name="groupmembers")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, default="Member")
    date_joined = models.DateField(default=date_today)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Active")

    def __str__(self):
        return f"{self.member.user.get_full_name()} in {self.group.name}"
