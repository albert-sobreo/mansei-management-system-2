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
from django.core.exceptions import PermissionDenied


class EMS_EmployeesView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        context = {
            'employees': request.user.branch.user.all(),
            'deminimises': DeMinimis.objects.all(),
        }
        return render(request, 'ems-employees.html', context)

class EMS_AddEmployee(APIView):
    def post(self, request):
        newHire = User.objects.create_user(idUser = request.data['idUser'], username=request.data['idUser'], password = "ManseiTechno", first_name = request.data['first_name'], 
        last_name = request.data['last_name'], position = request.data['position'], authLevel = request.data['authLevel'], 
        mobile = request.data['mobile'], email = request.data['email'], bloodType = request.data['bloodType'], rate = request.data['dailyRate'],
        tin = request.data['tin'], sss = request.data['sss'], phic = request.data['phic'], hdmf = request.data['hdmf'])

        newHire.branch = request.user.branch
        newHire.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_RaiseHistoryView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'ems-raise-history.html')


class AddBonus(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
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
        if request.user.authLevel == '2':
            raise PermissionDenied()
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
        if request.user.authLevel == '2':
            raise PermissionDenied()

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
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
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
        
class EMS_GivePromotion(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        data = request.data
        if not data['newPosition'] or not data['newRate']:
            sweetify.sweetalert(request, icon='error', title='Error!', text='Empty inputs'.format(data['newRate']), persistent='Dismiss')
            return JsonResponse(0, safe=False)
        user = User.objects.get(pk=data['user'])
        user.position = data['newPosition']
        user.rate = data['newRate']
        user.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class EMS_SaveEditBenefits(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        data = request.data
        user = User.objects.get(pk=data['user'])

        for myBenefit in user.deminimisofuser.all():
            myBenefit.delete()

        for benefit in data['deminimisofuser']:
            b = DeMinimisOfUser()
            b.user = user
            b.name = benefit['name']
            b.amount = benefit['amount']
            b.save()
            request.user.branch.deMinimisOfUser.add(b)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)