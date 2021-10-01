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

class EMS_MyPayslipView(View):
    def get(self, request):
        return render(request, 'ems-my-payslip.html')


class EMS_EmployeePayslipView(View):
    def get(self, request):
        return render(request, 'ems-employee-payslip.html')