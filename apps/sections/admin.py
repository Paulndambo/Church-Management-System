from django.contrib import admin

from apps.sections.models import Section, SectionReport, SectionMonthlyReport
from apps.users.models import Pastor


# Register your models here.
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "district", "created_at"]


@admin.register(Pastor)
class PastorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "church", "church__section", "pastor_role"]


@admin.register(SectionReport)
class SectionReportAdmin(admin.ModelAdmin):
    list_display = ["id", "section", "year", "district", "created_at"]



@admin.register(SectionMonthlyReport)
class SectionMonthlyReportAdmin(admin.ModelAdmin):
    list_display = ["id", "section_report", "month", "year", "created_at"]