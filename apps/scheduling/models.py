from django.db import models

from apps.core.models import AbstractBaseModel, Church
# Create your models here.
class Appointment(AbstractBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=255)
    town = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, default="Kenya")
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=255, default="Pending")
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)
    appointment_type = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def name(self):
        return f"{self.first_name} {self.last_name}"
    


class ChurchMeeting(AbstractBaseModel):
    title = models.CharField(max_length=255)
    meeting_date = models.DateTimeField()
    meeting_location = models.CharField(max_length=255)
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, default="Scheduled")

    def __str__(self):
        return self.title
    

class ChurchMeetingAttendance(AbstractBaseModel):
    meeting = models.ForeignKey(ChurchMeeting, on_delete=models.CASCADE, related_name="churchmeetingattendances")
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    status = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True)
    recorded_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def name(self):
        return f"{self.first_name} {self.last_name}"


REQUEST_TYPES = [
    ("Member", "Member"),
    ("Non-Member", "Non-Member"),
]

REQUEST_STATUSES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Complete", "Complete"),
    ("Declined", "Declined"),
    ("Cancelled", "Cancelled"),
]

GENDER_CHOICES=[
    ("Male", "Male"),
    ("Female", "Female"),
]

class BaptismRequest(AbstractBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    phone_number = models.CharField(max_length=255)
    request_type = models.CharField(max_length=255, choices=REQUEST_TYPES, default="Member")
    status = models.CharField(max_length=255, choices=REQUEST_STATUSES, default="Pending")
    request_date = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name
    

class MarriageRequest(AbstractBaseModel):
    groom_first_name = models.CharField(max_length=255)
    groom_last_name = models.CharField(max_length=255)
    bride_first_name = models.CharField(max_length=255)
    bride_last_name = models.CharField(max_length=255)
    wedding_date = models.DateField(max_length=255)
    wedding_location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    request_type = models.CharField(max_length=255, choices=REQUEST_TYPES, default="Member")
    status = models.CharField(max_length=255, choices=REQUEST_STATUSES, default="Pending")
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.groom_first_name
    

    def groom(self):
        return f"{self.groom_first_name} {self.groom_last_name}"

    def bride(self):
        return f"{self.bride_first_name} {self.bride_last_name}"

class BurialRequest(AbstractBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    phone_number = models.CharField(max_length=255)
    request_type = models.CharField(max_length=255, choices=REQUEST_TYPES, default="Member")
    status = models.CharField(max_length=255, choices=REQUEST_STATUSES, default="Pending")
    request_date = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name
    

class PrayerRequest(AbstractBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    phone_number = models.CharField(max_length=255)
    request_type = models.CharField(max_length=255, choices=REQUEST_TYPES, default="Member")
    status = models.CharField(max_length=255, choices=REQUEST_STATUSES, default="Pending")
    request_date = models.DateField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    month = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name