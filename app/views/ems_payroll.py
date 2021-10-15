from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
import pandas as pd
import json
from datetime import datetime

class EMS_PayrollView(View):
    def get(self, request):
        try: 
            y = request.GET['year']
            dateRange = request.GET['dateRange']
            dateStart = dateRange.split(' ')[0]
            dateEnd = dateRange.split(' ')[1]
            context = {
                'payrolls': request.user.branch.payroll.filter(year=y, dateStart=dateStart, dateEnd=dateEnd)
            }
        except Exception as e:
            print(e)
            context = {
                'payrolls': None
            }
        return render(request, 'ems-payroll.html', context)

class EMS_GeneratePayroll(APIView):
    def post(self, request):
        users = User.objects.filter(branch = request.user.branch)
        year = request.data[0]
        period = request.data[1]
        dateRange = request.data[2]

        dateStart = dateRange.split(' ')[0]
        dateEnd = dateRange.split(' ')[1]

        holidays = Holiday.objects.filter(date__range=[dateStart, dateEnd])
        print(holidays)

        for user in users:
            for dtr in user.dtr.filter(date__range=[dateStart, dateEnd]):
                print(dtr)

        return JsonResponse(0, safe=False)