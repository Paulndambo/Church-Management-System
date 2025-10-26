from django.contrib import admin

from apps.reports.models import ChurchMonthlyReport


# Register your models here.
@admin.register(ChurchMonthlyReport)
class ChurchMonthlyReportAdmin(admin.ModelAdmin):
    list_display = ["id", "branch", "month_name", "month_number", "created_at"]
