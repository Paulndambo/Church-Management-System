from django.contrib import admin

from apps.districts.models import District, KAGDistrictMonthlyReport, DistrictReport


# Register your models here.
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "church", "created_at"]


admin.site.register(KAGDistrictMonthlyReport)
admin.site.register(DistrictReport)