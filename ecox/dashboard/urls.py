from django.conf.urls import url
from django.contrib import admin
from .views import DashboardView

urlpatterns = [
    url(r'^$', DashboardView.as_view()),
]
