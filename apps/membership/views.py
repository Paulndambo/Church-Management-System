from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from apps.membership.models import Department, Branch, Member, ChurchService
from apps.users.models import User
from apps.core.constants import GENDER_CHOICES, USER_POSITIONS, STATUS_CHOICES
# Create your views here.

### Departments Management
@login_required
def departments(request):
    departments = Department.objects.all().order_by("-created_at")
    
    context = {
        "departments": departments
    }
    return render(request, "departments/departments.html", context)

@login_required
def new_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        
        Department.objects.create(
            name=name
        )
        
        return redirect("departments")
    return render(request, "departments/new_department.html")

@login_required
def edit_department(request):
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        department_name = request.POST.get("name")
        
        Department.objects.filter(id=department_id).update(
            name=department_name
        )
        return redirect("departments")
    return render(request, "departments/edit_department.html")


def delete_department(request):
    if request.method == "POST":
        department_id = request.POST.get("department_id")
        department = Department.objects.get(id=department_id)
        department.delete()
        return redirect("departments")
    return render(request, "departments/delete_department.html")

### Branches Management
@login_required
def branches(request):
    branches = Branch.objects.all().order_by("-created_at")
    
    context = {
        "branches": branches
    }
    return render(request, "branches/branches.html", context)


@login_required
def branch_details(request, id):
    branch = Branch.objects.get(id=id)
    
    
    context = {
        "branch": branch
    }
    
    return render(request, "branches/branch_details.html", context)

@login_required
def new_branch(request):
    if request.method == "POST":
        name = request.POST.get("name")
        town = request.POST.get("town")
        location = request.POST.get("location")
        
        print("**************Branch Data********")
        print(f"Name: {name}")
        print(f"Town: {town}")
        print(f"Location: {location}")
        print("**************Branch Data********")
        
        Branch.objects.create(
            name=name,
            location=location,
            town=town
        )
        
        
        return redirect("branches")
    return render(request, "branches/new_branch.html")

@login_required
def edit_branch(request):
    if request.method == "POST":
        branch_id = request.POST.get("branch_id")
        branch_name = request.POST.get("name")
        town = request.POST.get("town")
        location = request.POST.get("location")
        
        branch = Branch.objects.get(id=branch_id)
        branch.name = branch_name
        branch.town = town
        branch.location = location
        branch.save()
        return redirect("branches")
    return render(request, "branches/edit_branch.html")

@login_required
def delete_branch(request):
    if request.method == "POST":
        branch_id = request.POST.get("branch_id")
        branch = Department.objects.get(id=branch_id)
        branch.delete()
        return redirect("branches")
    return render(request, "branches/delete_branch.html")


### Services Management
@login_required
def church_services(request):
    services = ChurchService.objects.all().order_by("-created_at")
    
    context = {
        "services": services,
        "service_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }
    return render(request, "services/services.html", context)


@login_required
def new_church_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        starts_at = request.POST.get("starts_at")
        ends_at = request.POST.get("ends_at")
        service_day = request.POST.get("service_day")
        
        ChurchService.objects.create(
           name=name,
           service_day=service_day,
           starts_at=starts_at,
           ends_at=ends_at
        ) 
        
        return redirect("church-services")
    return render(request, "services/new_service.html")

@login_required
def edit_church_service(request):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        name = request.POST.get("name")
        starts_at = request.POST.get("starts_at")
        ends_at = request.POST.get("ends_at")
        service_day = request.POST.get("service_day")
        
        service = ChurchService.objects.get(id=service_id)
        service.name = name
        service.starts_at = starts_at
        service.ends_at = ends_at
        service.service_day = service_day
        service.save()
        return redirect("church-services")
    return render(request, "services/edit_service.html")

@login_required
def delete_church_service(request):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        service = ChurchService.objects.get(id=service_id)
        service.delete()
        return redirect("church-services")
    return render(request, "services/delete_service.html")

### Church Members Management
class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = "members/members_list.html"
    context_object_name = "members"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(user__id_number__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all()
        context["departments"] = Department.objects.all()
        context["gender_choices"] = GENDER_CHOICES
        context["positions"] = USER_POSITIONS
        context["status_choices"] = STATUS_CHOICES
        return context

@login_required
@transaction.atomic
def new_member(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        id_number = request.POST.get("id_number")
        department = request.POST.get("department")
        branch = request.POST.get("branch")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        role = request.POST.get("role")
        member_since = request.POST.get("member_since")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        
        email = email if email else f"{first_name}.{last_name}@gmail.com"
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            id_number=id_number,
            email=email,
            role=role,
            phone_number=phone_number,
            username=email,
            gender=gender,
            address=address,
            city=city,
            country=country
        )
        
        Member.objects.create(
            user=user,
            member_since=member_since,
            position=role,
            department_id=department,
            branch_id=branch,
            status="Active"
        )
        
        return redirect("members")
    return render(request, "members/new_membership.html")

@login_required
def edit_member(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        id_number = request.POST.get("id_number")
        department = request.POST.get("department")
        branch = request.POST.get("branch")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        role = request.POST.get("role")
        member_since = request.POST.get("member_since")
        member_status = request.POST.get("status")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        
        email = email if email else f"{first_name}.{last_name}@gmail.com"
        
        member = Member.objects.get(id=member_id)
        member.branch_id = branch
        member.department_id = department
        member.member_since = member_since
        member.status = member_status
        member.position = role
        member.save()
        
        member.user.first_name = first_name
        member.user.last_name = last_name
        member.user.email = email
        member.user.phone_number = phone_number
        member.user.id_number = id_number
        member.user.gender = gender
        member.user.address = address
        member.user.city = city
        member.user.country = country
        member.user.save()
        
        return redirect("members")
    return render(request, "members/edit_member.html")

@login_required
@transaction.atomic
def delete_member(request):
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        member = Member.objects.get(id=member_id)
        
        member.user.delete()
        member.delete()
        return redirect("members")
    return render(request, "members/delete_member.html")