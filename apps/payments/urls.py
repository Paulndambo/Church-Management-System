from django.urls import path

from apps.payments import views


urlpatterns = [
    path("offerings/", views.OfferingsListView.as_view(), name="offerings"),
    path("new-offering/", views.new_offering, name="new-offering"),
    path("edit-offering/", views.edit_offering, name="edit-offering"),
    
    path("tithings/", views.MemberTithingsListView.as_view(), name="tithings"),
    path("new-tithing/", views.new_member_tithing, name="new-tithing"),
    path("edit-tithing/", views.edit_member_tithing, name="edit-tithing"),
    
    path("department-savings/", views.DepartmentSavingsListView.as_view(), name="department-savings"),
    path("new-savings/", views.new_department_saving, name="new-savings"),
    path("edit-savings/", views.edit_department_saving, name="edit-savings"),
    
    path("expenses/", views.ChurchExpensesListView.as_view(), name="expenses"),
    path("new-expense/", views.new_expense, name="new-expense"),
    path("edit-expense/", views.edit_expense, name="edit-expense"),
    
    path("member-department-savings/", views.MemberDepartmentSavingsListView.as_view(), name="member-department-savings"),
    path("new-member-department-savings/", views.new_member_department_saving, name="new-member-department-savings"),
]
