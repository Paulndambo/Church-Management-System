from decimal import Decimal
from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.projects.models import Project, ProjectContribution, ProjectPledge
from apps.partners.models import ChurchPartner
from apps.membership.models import Member
from apps.payments.models import ChurchLedger
from apps.core.constants import get_month_name, get_month_number

# Create your views here.
date_today = datetime.now().date()

# Church Projects
class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/projects.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) | Q(name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_types"] = dict(Project._meta.get_field("project_type").choices)
        context["project_statuses"] = dict(Project._meta.get_field("status").choices)
        return context


@login_required
@transaction.atomic
def new_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        total_budget = request.POST.get("total_budget")
        amount_raised = request.POST.get("amount_raised")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        project_type = request.POST.get("project_type")
        status = request.POST.get("status")

        Project.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            total_budget=total_budget,
            amount_raised=amount_raised,
            project_type=project_type,
            status=status,
        )

        return redirect("projects")
    return render(request, "projects/new_project.html")


@login_required
@transaction.atomic
def edit_project(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        name = request.POST.get("name")
        total_budget = request.POST.get("total_budget")
        amount_raised = request.POST.get("amount_raised")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        project_type = request.POST.get("project_type")
        status = request.POST.get("status")

        Project.objects.filter(id=project_id).update(
            name=name,
            start_date=start_date,
            end_date=end_date,
            total_budget=total_budget,
            amount_raised=amount_raised,
            project_type=project_type,
            status=status,
        )

        return redirect("projects")
    return render(request, "projects/edit_project.html")


@login_required
def project_details(request: HttpRequest, id: int):
    project = Project.objects.get(id=id)

    contributions = ProjectContribution.objects.filter(project=project)
    pledges = ProjectPledge.objects.filter(project=project).order_by("-created_at")

    total_contributions = sum(list(contributions.values_list("amount", flat=True)))
    total_pledges = sum(list(pledges.values_list("amount_pledged", flat=True)))

    members = Member.objects.all()       

    context = {
        "project": project,
        "pledges": pledges,
        "total_contributions": total_contributions,
        "total_pledges": total_pledges,
        "members": members
    }
    return render(request, "projects/project_details.html", context)


## Church Project Contributions
class ProjectContributionsListView(LoginRequiredMixin, ListView):
    model = ProjectContribution
    template_name = "projects/contributions/contributions.html"
    context_object_name = "contributions"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(member__user__first_name__icontains=search_query)
                | Q(project__name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        context["members"] = Member.objects.all()
        return context


## Church Project Contributions Pledges
class ProjectPledgesListView(LoginRequiredMixin, ListView):
    model = ProjectPledge
    template_name = "projects/pledges/pledges.html"
    context_object_name = "pledges"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(member__user__first_name__icontains=search_query)
                | Q(project__name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = Member.objects.all()
        context["projects"] = Project.objects.all()
        context["partners"] = ChurchPartner.objects.all()
        return context


@login_required
@transaction.atomic
def new_pledge(request):
    if request.method == "POST":
        project = request.POST.get("project_id")
        member = request.POST.get("member")
        partner = request.POST.get("partner")
        amount_pledged = request.POST.get("amount_pledged")
        pledge_type = request.POST.get("pledge_type")

        month = get_month_name(date_today.month)

        print("***********Project ID***************")
        print(f"Project ID: {project}")
        print("***********Project ID***************")

        if pledge_type == "partner_pledge":
            ProjectPledge.objects.create(
                project_id=project,
                partner_id=partner if partner else None,
                amount_pledged=amount_pledged,
                month=month,
                year=date_today.year
            )
        elif pledge_type == "member_pledge":
            ProjectPledge.objects.create(
                project_id=project, member_id=member, amount_pledged=amount_pledged,
                month=month,
                year=date_today.year
            )

        return redirect("project-detail", id=project)
    return render(request, "projects/pledges/new_pledge.html")


@login_required
@transaction.atomic
def edit_pledge(request):
    if request.method == "POST":
        pledge_id = request.POST.get("pledge_id")
        amount_pledged = request.POST.get("amount_pledged")

        pledge = ProjectPledge.objects.get(id=pledge_id)
        pledge.amount_pledged=amount_pledged
        pledge.save()

        if Decimal(pledge.amount_redeemed) >= Decimal(pledge.amount_pledged):
            pledge.full_redeemed = True
            pledge.save()
        else:
            pledge.full_redeemed = False
            pledge.save()

        return redirect("project-detail", id=pledge.project.id)
    return render(request, "projects/pledges/edit_pledge.html")


@login_required
@transaction.atomic
def redeem_pledge(request):
    if request.method == "POST":
        pledge_id = request.POST.get("pledge_id")
        amount = request.POST.get("amount")

        pledge = ProjectPledge.objects.get(id=pledge_id)
        pledge.amount_redeemed += Decimal(amount)

        month = get_month_name(date_today.month)

        contribution = ProjectContribution.objects.create(
            project=pledge.project,
            member=pledge.member if pledge.member else None,
            partner=pledge.partner if pledge.partner else None,
            pledge=pledge,
            amount=amount,
            month=month,
            year=date_today.year
        )

        pledge.project.amount_raised += Decimal(amount)
        pledge.project.save()
        pledge.save()

        if Decimal(pledge.amount_redeemed) >= Decimal(pledge.amount_pledged):
            pledge.full_redeemed = True
            pledge.save()
        else:
            pledge.full_redeemed = False
            pledge.save()

        ChurchLedger.objects.create(
            name="Project Pledge Redemption",
            description=f"{contribution.member.user.name} Redeemed pledge for project {pledge.project.name}",
            amount=Decimal(amount),
            direction="Income",
            user=request.user,
            month=month,
            year=date_today.year
        )

        return redirect("project-detail", id=pledge.project.id)
    return render(request, "projects/pledges/redeem_pledge.html")
