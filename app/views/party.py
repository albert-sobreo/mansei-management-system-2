from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..serializers import *
from ..models import *

class VendorView(View):
    def get(self, request):
        context = {
            'customers': request.user.branch.party.filter(type='Customer')
        }
        return render(request, 'vendors.html')

class CustomerView(View):
    def get(self, request):
        return render(request, 'customers.html')