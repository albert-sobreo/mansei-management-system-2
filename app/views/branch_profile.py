import json
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..models import *
import sweetify

class BranchProfileView(View):
    def get(self, request, format=None):
        return render(request, 'branch-profile.html')

class SaveDefaultAccounts(APIView):
    def put(self, request, format=None):
        items = request.data
        print(items['pettyCash'])
        bdacct = BranchDefaultChildAccount.objects.get(pk=items['id'])
        try:
            bdacct.cashOnHand = AccountChild.objects.get(pk=items['cashOnHand'])
        except:
            pass
        try:
            bdacct.pettyCash = AccountChild.objects.get(pk=items['pettyCash'])
        except:
            pass
        try:
            bdacct.merchInventory = AccountChild.objects.get(pk=items['merchInventory'])
        except:
            pass
        try:
            bdacct.manuInventory = AccountChild.objects.get(pk=items['manuInventory'])
        except:
            pass
        try:
            bdacct.ppeProperty = AccountChild.objects.get(pk=items['manuInventory'])
        except:
            pass
        try:
            bdacct.ppePlant = AccountChild.objects.get(pk=items['ppePlant'])
        except:
            pass
        try:
            bdacct.ppeEquipment = AccountChild.objects.get(pk=items['ppeEquipment'])
        except:
            pass
        try:
            bdacct.inputVat = AccountChild.objects.get(pk=items['inputVat'])
        except:
            pass
        try:
            bdacct.outputVat = AccountChild.objects.get(pk=items['outputVat'])
        except:
            pass
        try:
            bdacct.ewp = AccountChild.objects.get(pk=items['ewp'])
        except:
            pass

        for item in items['cashInBank']:
            bdacct.cashInBank.add(AccountChild.objects.get(pk=item))

        for item in items['advancesToSupplier']:
            bdacct.advancesToSupplier = AccountChild.objects.get(pk=item)
        
        bdacct.save()
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

