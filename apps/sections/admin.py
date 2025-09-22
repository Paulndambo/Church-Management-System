from django.contrib import admin

from apps.sections.models import Section
# Register your models here.
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "district", "created_at"]