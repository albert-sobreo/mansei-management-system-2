from django import views
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from decimal import Decimal

class ReceivingReportView(View):
    def get(self, request, format=None):

        user = request.user

        try:
            rr = user.branch.receivingReport.latest('pk')

            listed_code = rr.code.split('-')
            listed_date = str(now.today()).split('-')

            cuprent_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                cuprent_code += 1
                new_code = 'RR-{}-{}-{}'.format(listed_date[0], listed_date[1], str(cuprent_code).zfill(4))
            else:
                new_code = 'RR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'RR-{}-{}-0001'.format(listed_date[0], listed_date[1])

        context = {
            'new_code': new_code,
        }
        return render(request, 'receiving-report.html', context)

class RRListView(View):
    def get(self, request, format=None):
        return render(request, 'rr-list.html')