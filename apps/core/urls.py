from django.urls import path

from apps.core.views import home, chart_data_api

urlpatterns = [
    path("", home, name="home"),
    path("api/chart-data/", chart_data_api, name="chart-data-api"),
]
