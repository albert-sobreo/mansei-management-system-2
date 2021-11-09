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
            dateStart = '1970-1-1'
            dateEnd = '1970-1-1'
        context = {
            'dtrs' : request.user.branch.dtr.filter(user=request.user, date__range=[dateStart, dateEnd]).order_by('-date')
        }
        return render(request, 'ems-my-timesheet.html', context)


class EMS_EmployeeTimesheetView(View):
    def get(self, request):
        try:
            user = User.objects.get(pk=request.GET['user'])
            y = request.GET['year']
            dateRange = request.GET['dateRange']
            dateStart = dateRange.split(' ')[0]
            dateEnd = dateRange.split(' ')[1]
        except Exception as e:
            print(e)
            user = request.user.branch.user.filter(payrollable=True).latest('pk')
            y = datetime.now().year
            dateStart = '{}-1-1'.format(y)
            dateEnd = '{}-12-31'.format(y)
            print(user, y, dateStart, dateEnd)
        
        context = {
            'employees': request.user.branch.user.filter(payrollable=True),
            'dtrs': request.user.branch.dtr.filter(user=user, date__range=[dateStart, dateEnd]).order_by('-date')
        }
        return render(request, 'ems-employee-timesheet.html', context)


class EMS_TimesheetTabularView(View):
    def get(self, request):
        return render(request, 'ems-timesheet-tabular.html')

class EMS_EditTimesheetHours(View):
    def post(self, request, pk, fromPage, params):
        print(pk, params)
        for val, keys in request.POST.items():
            print(val, keys)

        dtr = DTR.objects.get(pk=pk)
        dtr.bh = request.POST["bh"]
        dtr.ot = request.POST["ot"]
        dtr.nd = request.POST["nd"]
        dtr.ndot = request.POST["ndot"]
        dtr.rd = request.POST["rd"]
        dtr.rdot = request.POST["rdot"]
        dtr.rdnd = request.POST["rdnd"]
        dtr.rdndot = request.POST["rdndot"]
        dtr.rh = request.POST["rh"]
        dtr.rhot = request.POST["rhot"]
        dtr.rhnd = request.POST["rhnd"]
        dtr.rhndot = request.POST["rhndot"]
        dtr.sh = request.POST["sh"]
        dtr.shot = request.POST["shot"]
        dtr.shnd = request.POST["shnd"]
        dtr.shndot = request.POST["shndot"]
        dtr.shw = request.POST["shw"]
        dtr.shwot = request.POST["shwot"]
        dtr.shwnd = request.POST["shwnd"]
        dtr.shwndot = request.POST["shwndot"]
        dtr.rhrd = request.POST["rhrd"]
        dtr.rhrdot = request.POST["rhrdot"]
        dtr.rhrdnd = request.POST["rhrdnd"]
        dtr.rhrdndot = request.POST["rhrdndot"]
        dtr.shrd = request.POST["shrd"]
        dtr.shrdot = request.POST["shrdot"]
        dtr.shrdnd = request.POST["shrdnd"]
        dtr.shrdndot = request.POST["shrdndot"]
        dtr.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        if fromPage == 0:
            return redirect("/ems-my-timesheet/?{}".format(params))
        elif fromPage == 1:
            return redirect("/ems-employee-timesheet/?{}".format(params))