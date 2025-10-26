from django.contrib import admin

from apps.membership.models import Branch, Department, Member


# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "pastor", "section", "town", "location", "created_at"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "department",
        "branch",
        "position",
        "member_since",
        "created_at",
    ]
