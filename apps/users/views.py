from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.users.models import User, Visitor
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.db import transaction

from apps.membership.models import Department, Branch, Member
from apps.attendances.models import ChurchService
from apps.core.constants import GENDER_CHOICES, USER_POSITIONS, STATUS_CHOICES


# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print("***********User Information***************")
        print(username, password)
        print("***********User Information***************")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == "District Superintendent":
                next_url = request.GET.get("next", "district-home")
                return redirect(next_url)  # Redirect to the next URL or home page.
            next_url = request.GET.get("next", "home")
            return redirect(next_url)  # Redirect to the next URL or home page.
        else:
            return redirect("login")
    next_url = request.GET.get("next", "")
    return render(request, "accounts/login.html", {"next": next_url})


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")  # Redirect to a login page.


### Church Visitors Management
class VisitorListView(LoginRequiredMixin, ListView):
    model = Visitor
    template_name = "visitors/visitors.html"
    context_object_name = "visitors"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

        # Get sort parameter
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches"] = Branch.objects.all()
        context["members"] = Member.objects.all()
        context["church_services"] = ChurchService.objects.all()
        context["gender_choices"] = GENDER_CHOICES
        context["photo_consent_choices"] = ["Accept", "Decline"]
        return context


@login_required
@transaction.atomic
def new_visitor(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")

        branch = request.POST.get("branch")
        church_service = request.POST.get("church_service")
        brought_by = request.POST.get("brought_by")
        photo_consent = request.POST.get("photo_consent")

        Visitor.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            address=address,
            city=city,
            country=country,
            branch_id=branch,
            church_service_id=church_service,
            brought_by_id=brought_by,
            photo_consent=photo_consent,
        )

        return redirect("visitors")
    return render(request, "visitors/new_visitor.html")


@login_required
def edit_visitor(request):
    if request.method == "POST":
        visitor_id = request.POST.get("visitor_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")

        branch = request.POST.get("branch")
        church_service = request.POST.get("church_service")
        brought_by = request.POST.get("brought_by")
        photo_consent = request.POST.get("photo_consent")

        visitor = Visitor.objects.get(id=visitor_id)

        visitor.first_name = first_name
        visitor.last_name = last_name
        visitor.branch_id = branch
        visitor.phone_number = phone_number
        visitor.church_service_id = church_service
        visitor.gender = gender
        visitor.address = address
        visitor.city = city
        visitor.country = country
        visitor.photo_consent = photo_consent
        visitor.brought_by_id = brought_by
        visitor.save()

        return redirect("visitors")
    return render(request, "visitors/edit_visitor.html")


@login_required
@transaction.atomic
def delete_visitor(request):
    if request.method == "POST":
        visitor_id = request.POST.get("visitor_id")
        visitor = Visitor.objects.get(id=visitor_id)

        visitor.user.delete()
        visitor.delete()
        return redirect("visitors")
    return render(request, "visitors/delete_visitor.html")
