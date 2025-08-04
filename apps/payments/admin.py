from django.contrib import admin

from apps.payments.models import DepartmentSaving
# Register your models here.
@admin.register(DepartmentSaving)
class DepartmentSavingAdmin(admin.ModelAdmin):
    list_display = ["id", "department", "branch", "amount", "savings_date"]