from django.contrib import admin

from apps.events.models import ChurchEvent, EventTicketPayment, ChurchEventTicket
# Register your models here.
@admin.register(ChurchEventTicket)
class ChurchEventTicketAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "ticket_type", "paid_status"]
