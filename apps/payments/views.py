from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from decimal import Decimal

from apps.payments.models import (
    MemberTithing, DepartmentSaving, Offering, 
    ChurchExpense, MemberDepartmentSaving,
    ChurchLedger, ChurchDonation
)
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
       
        saving = DepartmentSaving.objects.create(
            department_id=department,
            branch_id=branch,
            amount=amount,
            savings_date=savings_date,
            captured_by=request.user
        )

        ChurchLedger.objects.create(
            name=f"{saving.department.name} Saving",
            description=f"Department Saving - {saving.department.name} - {saving.branch.name}",
            amount=Decimal(amount),
            direction="Income",
            user=request.user
        )
        
        return redirect("department-savings")
    return render(request, "department_savings/new_savings.html")


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
       
        tithe = MemberTithing.objects.create(
            member_id=member,
            amount=amount,
            tithing_date=tithing_date,
            captured_by=request.user
        )

        ChurchLedger.objects.create(
            name=f"{tithe.member.user.get_full_name()} Tithing",
            description=f"Tithing - {tithe.member.user.get_full_name()}",
            amount=Decimal(amount),
            direction="Income",
            user=request.user
        )
        
        return redirect("tithings")
    return render(request, "tithings/new_tithing.html")


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
       
        offering = Offering.objects.create(
            branch_id=branch,
            service_id=service,
            amount=amount,
            offering_date=offering_date,
            captured_by=request.user
        )
        
        ChurchLedger.objects.create(
            name=f"{offering.service.name} {offering_date} Offering",
            description=f"Offering - {offering.service.name} - {offering.branch.name}",
            amount=Decimal(amount),
            direction="Income",
            user=request.user
        )

        return redirect("offerings")
    return render(request, "offerings/new_offering.html")



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
       
        expense = ChurchExpense.objects.create(
            name=name,
            amount_allocated=amount_allocated,
            date_spend=date_spend,
            captured_by=request.user
        )

        ChurchLedger.objects.create(
            name=f"{expense.name} Expense",
            description=f"Expense - {expense.name}",
            amount=-abs(Decimal(amount_allocated)),
            direction="Expense",
            user=request.user
        )
        
        return redirect("expenses")
    return render(request, "expenses/new_expense.html")


### Church Ledger
class ChurchLedgerListView(LoginRequiredMixin, ListView):
    model = ChurchLedger
    template_name = "ledger/ledger.html"
    context_object_name = "ledger"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(name__icontains=search_query)
                | Q(direction__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


### Church Ledger
class ChurchDonationsListView(LoginRequiredMixin, ListView):
    model = ChurchDonation
    template_name = "donations/donations.html"
    context_object_name = "donations"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(donor__icontains=search_query)
                | Q(recorded_by__first_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

@login_required
@transaction.atomic
def new_church_donation(request):
    if request.method == "POST":
        donor = request.POST.get("donor")
        purpose = request.POST.get("purpose")
        
        amount = request.POST.get("amount")
        donation_date = request.POST.get("donation_date")
       
        donation = ChurchDonation.objects.create(
            donor=donor,
            purpose=purpose,
            amount=amount,
            donation_date=donation_date,
            captured_by=request.user
        )

        ChurchLedger.objects.create(
            name=f"{donation.donor} Donation",
            description=f"Donation: {donation.purpose}",
            amount=Decimal(amount),
            direction="Income",
            user=request.user
        )
        
        return redirect("donations")
    return render(request, "donations/new_donation.html")