from django.db import models
from decimal import Decimal
from apps.core.models import AbstractBaseModel

# Create your models here.
MESSAGE_TYPES = (
    ("SMS", "SMS"),
    ("EMAIL", "Email"),
    ("WhatsApp", "WhatsApp"),
)


class SMSSubscription(AbstractBaseModel):
    provider = models.CharField(max_length=100, null=True, blank=True)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    api_secret = models.CharField(max_length=255, null=True, blank=True)
    sender_id = models.CharField(max_length=100, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))

    def __str__(self):
        return f"{self.provider} - Balance: {self.balance}"


class UserMessage(AbstractBaseModel):
    title = models.CharField(max_length=255)
    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    scheduled = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    is_send = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="messages"
    )

    def __str__(self):
        return f"{self.title}"

    def send_status(self):
        return "Sent" if self.is_send else "Pending"

    def schedule_status(self):
        return "Scheduled" if self.scheduled else "Immediate"


class UserMessageRecipient(AbstractBaseModel):
    message = models.ForeignKey(
        UserMessage, on_delete=models.CASCADE, related_name="recipients"
    )
    recipient_phone_number = models.CharField(max_length=15, null=True, blank=True)
    recipient_email = models.EmailField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.message.title}"
