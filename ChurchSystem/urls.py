"""
URL configuration for ChurchSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("users/", include("apps.users.urls")),
    path("membership/", include("apps.membership.urls")),
    path("payments/", include("apps.payments.urls")),
    path("projects/", include("apps.projects.urls")),
    path("partners/", include("apps.partners.urls")),
    path("reports/", include("apps.reports.urls")),
    path("districts/", include("apps.districts.urls")),
    path("attendances/", include("apps.attendances.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("sections/", include("apps.sections.urls")),
    path("events/", include("apps.events.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
