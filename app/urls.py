from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()

########## CHART OF ACCOUNTS ##########
router.register(r"group", views.AccountGroupAPI, 'group')
router.register(r"sub-group", views.AccountSubGroupAPI, 'sub-group')
router.register(r"child", views.AccountChildAPI, 'child')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('', login_required(views.DashboardView.as_view())),
    path('chart-of-accounts/', login_required(views.ChartOfAccountsView.as_view())),
    path('journal/', login_required(views.JournalView.as_view())),
    path('save-journal/', login_required(views.SaveJournal.as_view())),
    path('ledger/', login_required(views.LedgerView.as_view())),
]