from django.db import models
from apps.core.models import AbstractBaseModel
from decimal import Decimal

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
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def status(self):
        return "Closed" if self.closed else "Open"
    

class ChurchEventTicketType(AbstractBaseModel):
    event = models.ForeignKey(ChurchEvent, on_delete=models.CASCADE, related_name="eventtickettypes")
    title = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    total_tickets = models.IntegerField()
    purchased = models.IntegerField(default=0)
    
    def __str__(self):
        return self.event.name
    

class ChurchEventTicket(AbstractBaseModel):
    ticket_number = models.CharField(max_length=255, null=True)
    event = models.ForeignKey(ChurchEvent, on_delete=models.CASCADE, related_name="eventtickets")
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    ticket_type = models.ForeignKey(ChurchEventTicketType, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))
    amount_paid = models.DecimalField(max_digits=100, decimal_places=2, default=Decimal('0'))

    def __str__(self):
        return self.event.name


class EventAttendance(AbstractBaseModel):
    event = models.ForeignKey(ChurchEvent, on_delete=models.CASCADE, related_name="eventattendances")
    ticket = models.ForeignKey(ChurchEventTicket, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, choices=(("Present", "Present"), ("Absent", "Absent"), ("Pending", "Pending")), default="Pending")
    checkin_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.event.name