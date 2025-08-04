from django.contrib import admin

from apps.membership.models import Branch, Department, Member, ChurchService
# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "town", "location", "created_at"]
    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    
    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "department", "branch", "position", "member_since", "created_at"]
    
    
@admin.register(ChurchService)
class ChurchServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "starts_at", "ends_at", "created_at"]