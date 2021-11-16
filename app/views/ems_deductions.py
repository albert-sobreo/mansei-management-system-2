from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime, date
import re
from .journalAPI import jeAPI

class EMS_SSSDeductionView(View):
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
            'payrolls': request.user.branch.payroll.filter(dateEnd = dateEnd)
        }
        return render(request, 'ems-sss-page.html', context)

class EMS_PHICDeductionView(View):
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
            'payrolls': request.user.branch.payroll.filter(dateEnd = dateEnd)
        }
        return render(request, 'ems-phic-page.html', context)

class EMS_HDMFDeduction(View):
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
            'payrolls': request.user.branch.payroll.filter(dateEnd = dateEnd)
        }
        return render(request, 'ems-hdmf-page.html', context)

class EMS_TaxDeduction(View):
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
            'payrolls': request.user.branch.payroll.filter(dateEnd = dateEnd)
        }
        return render(request, 'ems-taxes-page.html', context)

class EMS_SSSLoanDeduction(View):
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
            'payrolls': request.user.branch.payroll.filter(dateEnd = dateEnd)
        }
        return render(request, 'ems-sss-loan-deduction.html', context)