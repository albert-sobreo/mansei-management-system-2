from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..models import *
from datetime import date as now
from datetime import datetime
from datetime import timedelta

class LedgerView(View):
    def get(self, request):
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        
        except:
            startDate = now.today().replace(day=1)
            nextMonth = now.today().replace(month=startDate.month+1, day=1)
            endDate = nextMonth - timedelta(days=1)

        context = {
            'children': request.user.branch.accountChild.all(),
            'startDate': startDate,
            'endDate': endDate,
            'date': str(startDate)+ ',' +str(endDate)
        }
        return render(request, 'ledger.html', context)