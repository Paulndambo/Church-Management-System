from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpRequest
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from apps.membership.models import Branch
from apps.users.models import Pastor
from apps.core.constants import GENDER_CHOICES
from apps.sections.models import Section


class PastorsListView(LoginRequiredMixin, ListView):
    model = Pastor
    template_name = "districts/pastors/pastors.html"
    context_object_name = "pastors"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
    
        section_id = self.request.GET.get("section")
        
        if section_id:
            queryset = queryset.filter(church__section__id=section_id)
        
        # Get sort parameter
        return queryset.exclude(pastor_role="Pastor Associate").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all()
        context["genders"] = GENDER_CHOICES
        context["pastor_roles"] = ["Lead Pastor", "Pastor Associate"]
        context["sections"] = Section.objects.all()
        return context
    

@login_required
@transaction.atomic
def new_pastor(request: HttpRequest):
    if request.method == "POST":
        branch = request.POST.get("branch")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
       

        Pastor.objects.create(
            church_id=branch,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            email=email,
            pastor_role="Lead Pastor"
        )
        return redirect("district-pastors")
    return render(request, "districts/pastors/new_pastor.html")


@login_required
def edit_pastor(request: HttpRequest):
    if request.method == "POST":
        pastor_id = request.POST.get("pastor_id")
        branch = request.POST.get("branch")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        pastor_role = request.POST.get("pastor_role")


        Pastor.objects.filter(id=pastor_id).update(
            church_id=branch,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            email=email,
            pastor_role=pastor_role
        )
        return redirect("district-pastors")
    return render(request, "districts/pastors/edit_pastor.html")


@login_required
def delete_pastor(request: HttpRequest):
    if request.method == "POST":
        pastor_id = request.POST.get("pastor_id")
        role = request.POST.get("role")

        pastor = Pastor.objects.get(id=pastor_id)
        pastor.delete()

        print("***************Pastor Role*****************")
        print(f"Role: {role}")
        print("***************Pastor Role*****************")

        if role == "Lead Pastor":
            return redirect("district-pastors")
        
        return redirect("district-pastor-associates")

    return render(request, "districts/pastors/delete_pastor.html")


class PastorsAssociatesListView(LoginRequiredMixin, ListView):
    model = Pastor
    template_name = "districts/pastors/pastor_associates.html"
    context_object_name = "pastors"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        section_id = self.request.GET.get("section")

        if section_id:
            queryset = queryset.filter(church__section_id=section_id)
        # Get sort parameter
        return queryset.filter(pastor_role="Pastor Associate").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all()
        context["sections"] = Section.objects.all()
        return context
    

@login_required
@transaction.atomic
def new_pastor_associate(request: HttpRequest):
    if request.method == "POST":
        branch = request.POST.get("branch")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
    
        Pastor.objects.create(
            church_id=branch,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            email=email,
            pastor_role="Pastor Associate"
        )
        return redirect("district-pastor-associates")
    return render(request, "districts/pastors/new_pastor_associate.html")


@login_required
def edit_pastor_associate(request: HttpRequest):
    if request.method == "POST":
        pastor_id = request.POST.get("pastor_id")
        branch = request.POST.get("branch")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")

        Pastor.objects.filter(id=pastor_id).update(
            church_id=branch,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
            email=email,
            pastor_role="Pastor Associate"
        )
        return redirect("district-pastor-associates")
    return render(request, "districts/pastors/edit_pastor_associate.html")