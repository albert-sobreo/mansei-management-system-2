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

class EMS_MyTimesheetView(View):
    def get(self, request):
        try:
            y = request.GET['year']
            dateRange = request.GET['dateRange']
            dateStart = dateRange.split(' ')[0]
            dateEnd = dateRange.split(' ')[1]
        except Exception as e:
            print(e)
            y = datetime.now().year
            dateStart = '{}-1-1'.format(y)
            dateEnd = '{}-12-31'.format(y)
        context = {
            'dtrs' : request.user.branch.dtr.filter(user=request.user, date__range=[dateStart, dateEnd]).order_by('-date')
        }
        return render(request, 'ems-my-timesheet.html', context)


class EMS_EmployeeTimesheetView(View):
    def get(self, request):
        return render(request, 'ems-employee-timesheet.html')


class EMS_TimesheetTabularView(View):
    def get(self, request):
        return render(request, 'ems-timesheet-tabular.html')