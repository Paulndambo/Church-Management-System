from django.contrib import admin

from apps.core.models import UserActionLog, Church
# Register your models here.
@admin.register(UserActionLog)
class UserActionLog(admin.ModelAdmin):
    list_display = ["id", "user", "action_type", "created_at"]


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]