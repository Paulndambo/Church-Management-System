from django.db import models
from apps.core.models import AbstractBaseModel
# Create your models here.
CHURCH_EVENT_TYPES = (
    ("Paid Event", "Paid Event"),
    ("Free Event", "Free Event"),
)
class ChurchEvent(AbstractBaseModel):
    name = models.CharField(max_length=255)
    poster_image = models.ImageField(upload_to="event_posters", null=True)
    description = models.TextField(null=True)
    event_type = models.CharField(max_length=255, choices=CHURCH_EVENT_TYPES)
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()
    
    def __str__(self):
        return self.name


class EventAttendance(AbstractBaseModel):
    event = models.ForeignKey(ChurchEvent, on_delete=models.CASCADE)
    member = models.ForeignKey("membership.Member", on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.event.name