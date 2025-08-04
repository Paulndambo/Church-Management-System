from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from decimal import Decimal

from apps.payments.models import MemberTithing, DepartmentSaving, Offering, ChurchExpense, MemberDepartmentSaving
from apps.membership.models import Member, Department, Branch, ChurchService

date_today = datetime.now().date()
# Create your views here.
### Department Savings
class DepartmentSavingsListView(LoginRequiredMixin, ListView):
    model = DepartmentSaving
    template_name = "department_savings/savings.html"
    context_object_name = "savings"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(department__name__icontains=search_query)
                | Q(captured_by__first_name__icontains=search_query)
                | Q(captured_by__last_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        context["branches"] = Branch.objects.all()
        return context


@login_required
@transaction.atomic
def new_department_saving(request):
    if request.method == "POST":
        department = request.POST.get("department")
        branch = request.POST.get("branch")
        
        amount = request.POST.get("amount")
        savings_date = request.POST.get("savings_date")
       
        DepartmentSaving.objects.create(
            department_id=department,
            branch_id=branch,
            amount=amount,
            savings_date=savings_date,
            captured_by=request.user
        )
        
        return redirect("department-savings")
    return render(request, "department_savings/new_savings.html")


@login_required
@transaction.atomic
def edit_department_saving(request):
    if request.method == "POST":
        savings_id = request.POST.get("savings_id")
        department = request.POST.get("department")
        branch = request.POST.get("branch")
        
        amount = request.POST.get("amount")
        savings_date = request.POST.get("savings_date")
       
        DepartmentSaving.objects.filter(id=savings_id).update(
            department_id=department,
            branch_id=branch,
            amount=amount,
            savings_date=savings_date,
            captured_by=request.user
        )
        
        return redirect("department-savings")
    return render(request, "department_savings/edit_savings.html")


class MemberDepartmentSavingsListView(LoginRequiredMixin, ListView):
    model = MemberDepartmentSaving
    template_name = "department_savings/member_savings.html"
    context_object_name = "savings"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(department__name__icontains=search_query)
                | Q(member__first_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = Member.objects.all()
        return context


@login_required
@transaction.atomic
def new_member_department_saving(request):
    if request.method == "POST":
        member = request.POST.get("member")
        amount = request.POST.get("amount")
        
        member = Member.objects.get(id=member)
        
        d_saving = DepartmentSaving.objects.filter(
            department=member.department, 
            branch=member.branch
        ).first()
        
        if not d_saving:
            d_saving = DepartmentSaving.objects.create(
                department=member.department,
                branch=member.branch,
                amount=0,
                savings_date=date_today,
                captured_by=request.user
            )
        
        d_saving.amount += Decimal(amount)
        d_saving.save()
        
        MemberDepartmentSaving.objects.create(
            member=member,
            amount=Decimal(amount),
            savings_date=date_today,
            captured_by=request.user
        )
        
        return redirect("member-department-savings")
    return render(request, "department_savings/member_department_saving.html")



@login_required
@transaction.atomic
def edit_member_department_saving(request):
    if request.method == "POST":
        savings_id = request.POST.get("savings")
        member = request.POST.get("member")
        amount = request.POST.get("amount")
        
        m_saving = MemberDepartmentSaving.objects.get(id=savings_id)
        
        
        member = Member.objects.get(id=member)
        
        d_saving = DepartmentSaving.objects.filter(
            department=member.department, 
            branch=member.branch
        ).first()
        
        if not d_saving:
            d_saving = DepartmentSaving.objects.create(
                department=member.department,
                branch=member.branch,
                amount=0,
                savings_date=date_today,
                captured_by=request.user
            )
        
        d_saving.amount += Decimal(amount)
        d_saving.save()
        
        MemberDepartmentSaving.objects.create(
            member=member,
            amount=Decimal(amount),
            savings_date=date_today,
            captured_by=request.user
        )
        
        return redirect("member-department-savings")
    return render(request, "department_savings/member_department_saving.html")


### Member Tithings
class MemberTithingsListView(LoginRequiredMixin, ListView):
    model = MemberTithing
    template_name = "tithings/tithings.html"
    context_object_name = "tithings"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(member__user__first_name__icontains=search_query)   
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = Member.objects.all()
        return context


@login_required
@transaction.atomic
def new_member_tithing(request):
    if request.method == "POST":
        member = request.POST.get("member")
        amount = request.POST.get("amount")
        tithing_date = request.POST.get("tithing_date")
       
        MemberTithing.objects.create(
            member_id=member,
            amount=amount,
            tithing_date=tithing_date,
            captured_by=request.user
        )
        
        return redirect("tithings")
    return render(request, "tithings/new_tithing.html")


@login_required
@transaction.atomic
def edit_member_tithing(request):
    if request.method == "POST":
        tithing_id = request.POST.get("tithing_id")
        member = request.POST.get("member")
        amount = request.POST.get("amount")
        tithing_date = request.POST.get("tithing_date")
        
        tithing = MemberTithing.objects.get(id=tithing_id)
        tithing.member_id=member
        tithing.amount=amount
        tithing.tithing_date=tithing_date
        tithing.captured_by=request.user
        tithing.save()
        
        return redirect("tithings")
    return render(request, "tithings/edit_tithing.html")



### Service Offerings
class OfferingsListView(LoginRequiredMixin, ListView):
    model = Offering
    template_name = "offerings/offerings.html"
    context_object_name = "offerings"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(service__name__icontains=search_query)
                | Q(branch__name__icontains=search_query)    
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all()
        context["services"] = ChurchService.objects.all()
        return context


@login_required
@transaction.atomic
def new_offering(request):
    if request.method == "POST":
        branch = request.POST.get("branch")
        service = request.POST.get("service")
        amount = request.POST.get("amount")
        offering_date = request.POST.get("offering_date")
       
        Offering.objects.create(
            branch_id=branch,
            service_id=service,
            amount=amount,
            offering_date=offering_date,
            captured_by=request.user
        )
        
        return redirect("offerings")
    return render(request, "offerings/new_offering.html")


@login_required
@transaction.atomic
def edit_offering(request):
    if request.method == "POST":
        offering_id = request.POST.get("offering_id")
        branch = request.POST.get("branch")
        service = request.POST.get("service")
        amount = request.POST.get("amount")
        offering_date = request.POST.get("offering_date")
       
        Offering.objects.filter(id=offering_id).update(
            branch_id=branch,
            service_id=service,
            amount=amount,
            offering_date=offering_date,
            captured_by=request.user
        )
        
        return redirect("offerings")
    return render(request, "offerings/edit_offering.html")



### Church Expenses
class ChurchExpensesListView(LoginRequiredMixin, ListView):
    model = ChurchExpense
    template_name = "expenses/expenses.html"
    context_object_name = "expenses"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
@transaction.atomic
def new_expense(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount_allocated = request.POST.get("amount_allocated")
        date_spend = request.POST.get("date_spend")
       
        ChurchExpense.objects.create(
            name=name,
            amount_allocated=amount_allocated,
            date_spend=date_spend,
            captured_by=request.user
        )
        
        return redirect("expenses")
    return render(request, "expenses/new_expense.html")


@login_required
@transaction.atomic
def edit_expense(request):
    if request.method == "POST":
        expense_id = request.POST.get("expense_id")
        name = request.POST.get("name")
        amount_allocated = request.POST.get("amount_allocated")
        date_spend = request.POST.get("date_spend")
       
        ChurchExpense.objects.filter(id=expense_id).update(
            name=name,
            amount_allocated=amount_allocated,
            date_spend=date_spend,
            captured_by=request.user
        )
        
        return redirect("expenses")
    return render(request, "expenses/edit_expense.html")