from django.db import models
from apps.core.models import AbstractBaseModel


# Create your models here.
class ChurchPartner(AbstractBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    occupation = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
