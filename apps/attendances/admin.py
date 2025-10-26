from django.contrib import admin

from apps.attendances.models import (
    ServiceAttendance,
    ServiceAttendanceMetric,
    ChurchService,
)


# Register your models here.
@admin.register(ServiceAttendance)
class ServiceAttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "member", "service", "status", "month", "year", "created_at"]
    list_filter = ["month", "year"]


@admin.register(ServiceAttendanceMetric)
class ServiceAttendanceMetricAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "branch",
        "service",
        "total_present",
        "service_date",
        "month",
        "year",
        "created_at",
    ]
    list_filter = ["month", "year"]


@admin.register(ChurchService)
class ChurchServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "starts_at", "ends_at", "created_at"]
