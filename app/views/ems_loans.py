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
import datetime
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class EMS_SSSLoansView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        try:
            user = User.objects.get(pk=request.GET['user'])
            y = request.GET['year']
        except Exception as e:
            print(e)
            user = request.user.branch.user.filter(payrollable=True).latest('pk')
            y = datetime.datetime.now().year

        context = {
            'employees': request.user.branch.user.filter(payrollable=True),
            'loans': request.user.branch.loans.filter(user=user, year=y, loanFrom="SSS")
        }
        return render(request, 'ems-sss-loans.html', context)

class EMS_HDMFLoansView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        try:
            user = User.objects.get(pk=request.GET['user'])
            y = request.GET['year']
        except Exception as e:
            print(e)
            user = request.user.branch.user.filter(payrollable=True).latest('pk')
            y = datetime.datetime.now().year

        context = {
            'employees': request.user.branch.user.filter(payrollable=True),
            'loans': request.user.branch.loans.filter(user=user, year=y, loanFrom="HDMF")
        }
        return render(request, 'ems-hdmf-loans.html', context)

class EMS_LoanCreate(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        data =  request.data
        print(data)

        loan = Loans()
        loan.user = request.user.branch.user.get(pk=data['user']['id'])
        loan.dateCreated = datetime.date.today()
        loan.year = data['startOfAmortization'].split('-')[0]
        loan.startOfAmortization = data['startOfAmortization']
        loan.endOfAmortization = data['endOfAmortization']
        loan.loanType = data['loanType']
        loan.loanFrom = data['loanFrom']
        loan.loanAmount = data['loanAmount']
        loan.serviceFee = data['serviceFee']
        loan.serviceFeeRate = data['serviceFeeRate']
        loan.netProceeds = data['netProceeds']
        loan.interestAmount = data['interestAmount']
        loan.interestRate = data['interestRate']
        loan.totalWithInterest = data['totalWithInterest']
        loan.monthlyAmortization = data['monthlyAmortization']
        loan.save()
        request.user.branch.loans.add(loan)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)