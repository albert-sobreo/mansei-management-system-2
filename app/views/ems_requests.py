from rest_framework import views
from rest_framework.views import APIView
from ..models import MerchandiseInventory, Warehouse, WarehouseItems
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime

class EMS_OvertimeRequestsView(View):
    def get(self, request):
        return render(request, 'ems-overtime-request.html')

class EMS_UndertimeRequestsView(View):
    def get(self, request):
        return render(request, 'ems-undertime-request.html')

class EMS_LeaveRequestsView(View):
    def get(self, request):
        return render(request, 'ems-leave-request.html')