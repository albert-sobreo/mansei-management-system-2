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
from datetime import datetime, date
from ..models import*


class EMS_EmployeesView(View):
    def get(self, request):
        context = {
            'employees': request.user.branch.user.all(),
            'deminimises': DeMinimis.objects.all(),
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

class GiveDeMinimis(APIView):
    def post(self, request):
        for benefits in request.data['benefits']:
            dm = DeMinimisOfUser()
            dm.user = User.objects.get(pk=request.data['user'])
            dm.name = DeMinimis.objects.get(pk=benefits['pk'])
            dm.amount = Decimal(benefits['amount'])
            dm.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class AddDeMinimis(APIView):
    def post(self, request):

        for benefit in request.data['benefits']:
            dm = DeMinimisOfUser()
            dm.user = User.objects.get(benefit['pk'])
            dm.name = benefit['name']
            dm.amount = benefit['amount']
            dm.save()
            request.user.branch.deMinimisOfUser.add()
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_GiveRaise(APIView):
    def post(self, request):
        data = request.data
        if not data['newRate']:
            sweetify.sweetalert(request, icon='error', title='Error!', text='New Rate is {}'.format(data['newRate']), persistent='Dismiss')
            return JsonResponse(0, safe=False)
        user = User.objects.get(pk=data['user'])
        r = Raise()
        r.user = user
        r.previousRate = r.user.rate
        r.newRate = data['newRate']
        r.date = date.today()
        r.save()
        request.user.branch.race.add(r)

        user.rate = data['newRate']
        user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
        