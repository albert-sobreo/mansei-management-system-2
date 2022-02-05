from ..models import *
from django.shortcuts import render
from django.views import View
from ..forms import *
from datetime import datetime
from django.core.exceptions import PermissionDenied

class EMS_SSSDeductionView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
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
        if request.user.authLevel == '2':
            raise PermissionDenied()
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
        if request.user.authLevel == '2':
            raise PermissionDenied()
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
        if request.user.authLevel == '2':
            raise PermissionDenied()
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
        if request.user.authLevel == '2':
            raise PermissionDenied()
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