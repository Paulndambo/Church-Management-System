from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models import AbstractBaseModel

# Create your models here.
USER_ROLES = (
    ("Church Member", "Church Member"),
    ("Pastor", "Pastor"),
    ("Men Department Leader", "Men Department Leader"),
    ("Women Department Leader", "Women Department Leader"),
    ("Teens Department Leader", "Teens Department Leader"),
    ("Church Secretary", "Church Secretary"),
    ("Church Treasurer", "Church Treasurer"),
    ("District Supritendant", "District Supritendant"),
    ("Presbyter", "Presbyter"),
    ("Church Usher", "Church Usher"),
)

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class User(AbstractUser, AbstractBaseModel):
    role = models.CharField(max_length=255, choices=USER_ROLES, default="Church Member")
    phone_number = models.CharField(max_length=255, null=True)
    id_number = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    branch = models.ForeignKey(
        "membership.Branch", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.username

    def name(self):
        return self.get_full_name()


class Visitor(AbstractBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    photo_consent = models.CharField(
        max_length=255, choices=(("Accept", "Accept"), ("Decline", "Decline"))
    )
    brought_by = models.ForeignKey(
        "membership.Member", on_delete=models.SET_NULL, null=True
    )
    branch = models.ForeignKey(
        "membership.Branch", on_delete=models.SET_NULL, null=True
    )
    church_service = models.ForeignKey(
        "attendances.ChurchService", on_delete=models.SET_NULL, null=True
    )
    times_attended = models.IntegerField(default=1)
    converted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Pastor(AbstractBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    is_active = models.BooleanField(default=True)
    church = models.OneToOneField("membership.Branch", on_delete=models.SET_NULL, null=True, related_name="churchpastor")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"