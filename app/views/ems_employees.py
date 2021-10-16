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
from ..models import*

class EMS_EmployeesView(View):
    def get(self, request):
        context = {
            'employees': request.user.branch.user.all()
        }
        return render(request, 'ems-employees.html', context)


class EMS_RaiseHistoryView(View):
    def get(self, request):
        return render(request, 'ems-raise-history.html')


class AddBonus(APIView):
    def post(self, request, format = None):
        
        for benefit in request.data['bonuses']:
            bonus = BonusOfUser()
            bonus.user = User.objects.get(request.data['pk'])
            bonus.name = benefit['name']
            bonus.amount = benefit['amount']
            bonus.save()
            request.user.branch.bonusOfUser.add()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class AddDeMinimis(APIView):
    def post(self, request, formnat = None):

        for benefit in request.data['benefits']:
            dm = DeMinimisOfUser()
            dm.user = User.objects.get(request.data['pk'])
            dm.name = request.data['name']
            dm.amount = request.data['amount']
            dm.save()
            request.user.branch.deMinimisOfUser.add()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)