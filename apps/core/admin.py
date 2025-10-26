from django.contrib import admin

from apps.core.models import UserActionLog, Church, Country, ChurchRole


# Register your models here.
@admin.register(UserActionLog)
class UserActionLog(admin.ModelAdmin):
    list_display = ["id", "user", "action_type", "created_at"]


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]



@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "currency", "currency_code", "created_at"]


@admin.register(ChurchRole)
class ChurchRoleAdmin(admin.ModelAdmin):
    list_display = ["id", "church", "name", "leadership_role", "created_at"]