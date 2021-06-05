from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('', login_required(views.DashboardView.as_view())),
    path('chart-of-accounts/', login_required(views.ChartOfAccountsView.as_view())),
]