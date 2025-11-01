from django.contrib import admin

from apps.districts.models import District, KAGDistrictMonthlyReport, DistrictReport


# Register your models here.
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "church", "created_at"]


@admin.register(KAGDistrictMonthlyReport)
class KAGDistrictMonthlyReportAdmin(admin.ModelAdmin):
    list_display = ["id", "district", "section", "section_report", "year", "month", "created_at"]
    search_fields = ["month"]

@admin.register(DistrictReport)
class DistrictReportAdmin(admin.ModelAdmin):
    list_display = ["id", "district", "month", "year"]