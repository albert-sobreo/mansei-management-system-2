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
from django.core.exceptions import PermissionDenied
from .notificationCreate import *
from .journalAPI import JournalAPI, getNewJournalCode

class EMS_MyPayslipView(View):
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
        try:
            context = {
                'payslips': request.user.branch.payslip.get(user=request.user, payroll__dateStart=dateStart, payroll__dateEnd=dateEnd)
            }
        except:
            context = {
                'payslips': 0
            }
        return render(request, 'ems-my-payslip.html', context)


class EMS_EmployeePayslipView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
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
        
        try:
            context = {
                'employees': request.user.branch.user.filter(payrollable=True),
                'payslips': request.user.branch.payslip.get(user=user, payroll__dateStart=dateStart, payroll__dateEnd=dateEnd)
            }
        except:
            context = {
                'employees': request.user.branch.user.filter(payrollable=True),
                'payslips': 0
            }
        return render(request, 'ems-employee-payslip.html', context)

class ReceivePayslipSolo(APIView):
    def post(self, request):
        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount
        if request.user.authLevel == '2':
            raise PermissionDenied()
        payslip = Payslip.objects.get(pk=request.data['id'])
        if payslip.received == True:
            sweetify.sweetalert(request, icon='warning', title='Payslip has been received already!', persistent='Dismiss')
            return JsonResponse(0, safe=False)
        else:
            payslip.received = True
            j = JournalAPI(request, getNewJournalCode(request), request.user, datetime.now())
            j.addJE('Credit', dChildAccount.cashInBankForPayroll, payslip.payroll.netPayAfterTaxes)
            j.addJE('Debit', dChildAccount.salariesPayable, payslip.payroll.netPayAfterTaxes)
            payslip.save()
            j.save()

        notify(request, 'Payslip Received', f'Payslip of {payslip.payroll.user.first_name} {payslip.payroll.user.first_name} for the period {payslip.payroll.dateStart} - {payslip.payroll.dateEnd} has been approved', '/ems-payslip/', 1)
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)



        # DATA SENT FROM FRONTEND
        # user pk
        # year
        # dateStart
        # dateEnd
        
        # OR
        # FRONTEND WILL SEND PAYROLL/PAYSLIP OBJECT ID

class ReceivePayslipBulk(APIView):
    pass