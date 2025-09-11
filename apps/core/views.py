from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.membership.models import Member
from apps.payments.models import MemberTithing, Offering, DepartmentSaving
from apps.projects.models import ProjectContribution, ProjectPledge, Project
# Create your views here.
@login_required
def home(request):
    if request.user.role == "Distric Supritendant":
        return redirect("district-reports")
    total_members = Member.objects.count()
    total_department_savings = sum(DepartmentSaving.objects.values_list("amount", flat=True))
    tithes_total = sum(MemberTithing.objects.values_list("amount", flat=True))
    total_offerings = sum(Offering.objects.values_list("amount", flat=True))
    
    projects_pledges = sum(ProjectPledge.objects.values_list("amount_pledged", flat=True))
    projects_contributions = sum(ProjectContribution.objects.values_list("amount", flat=True))
    
    context = {
        "total_members": total_members,
        "total_department_savings": total_department_savings,
        "tithes_total": tithes_total,
        "total_offerings": total_offerings,
        "projects_pledges": projects_pledges,
        "projects_contributions": projects_contributions
    }
    return render(request, "home.html", context)