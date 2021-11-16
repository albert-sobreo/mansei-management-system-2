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

class EMS_SSSLoansView(View):
    def get(self, request):
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