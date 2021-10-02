from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime
import re
from .journalAPI import jeAPI

class EMS_OvertimePendingView(View):
    def get(self, request):
        return render(request, 'ems-overtime-pending.html')

class EMS_OvertimeApprovedView(View):
    def get(self, request):
        return render(request, 'ems-overtime-approved.html')

class EMS_UndertimePendingView(View):
    def get(self, request):
        return render(request, 'ems-undertime-pending.html')

class EMS_UndertimeApprovedView(View):
    def get(self, request):
        return render(request, 'ems-undertime-approved.html')

class EMS_LeavePendingView(View):
    def get(self, request):
        return render(request, 'ems-leave-pending.html')

class EMS_LeaveApprovedView(View):
    def get(self, request):
        return render(request, 'ems-leave-approved.html')