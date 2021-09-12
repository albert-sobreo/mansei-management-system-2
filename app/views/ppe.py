from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from datetime import datetime
from decimal import Decimal

class PPEView(View):
    def get(self, request):
        return render(request, 'ppe.html')