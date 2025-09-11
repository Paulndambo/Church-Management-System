from django.contrib import admin

from apps.payments.models import DepartmentSaving, ChurchLedger, MemberTithing, ChurchDonation
# Register your models here.
@admin.register(DepartmentSaving)
class DepartmentSavingAdmin(admin.ModelAdmin):
    list_display = ["id", "department", "branch", "amount", "savings_date"]


@admin.register(ChurchLedger)
class ChurchLedgerAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "amount", "direction", "created_at",]


@admin.register(MemberTithing)
class MemberTithingAdmin(admin.ModelAdmin):
    list_display = ["id", "member", "amount", "tithing_date", "captured_by"]


@admin.register(ChurchDonation)
class ChurchDonationAdmin(admin.ModelAdmin):
    list_display = ["id", "donor", "amount", "donation_date", "captured_by"]