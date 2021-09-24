
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *
import sweetify

class BranchProfileView(View):
    def get(self, request, format=None):
        context = {
            'sg': request.user.branch.subGroup.all()
        }
        return render(request, 'branch-profile.html', context)

class SaveDefaultAccounts(APIView):
    def put(self, request, format=None):
        items = request.data
        print(items['pettyCash'])
        bdacct = BranchDefaultChildAccount.objects.get(pk=items['id'])
        try:
            bdacct.rm = AccountChild.objects.get(pk=items['rm'])
        except Exception as e:
            print(e)
            bdacct.rm = None
        try:
            bdacct.defaultWarehouse = Warehouse.objects.get(pk=items['defaultWarehouse'])
        except Exception as e:
            print(e)
            bdacct.defaultWarehouse = None
        try:
            bdacct.cashOnHand = AccountChild.objects.get(pk=items['cashOnHand'])
        except Exception as e:
            print(e)
            bdacct.cashOnHand = None
        try:
            bdacct.pettyCash = AccountChild.objects.get(pk=items['pettyCash'])
        except Exception as e:
            print(e)
            bdacct.pettyCash = None
        try:
            bdacct.merchInventory = AccountChild.objects.get(pk=items['merchInventory'])
        except Exception as e:
            print(e)
            bdacct.merchInventory = None
        try:
            bdacct.manuInventory = AccountChild.objects.get(pk=items['manuInventory'])
        except Exception as e:
            print(e)
            bdacct.manuInventory = None
        try:
            bdacct.ppeProperty = AccountChild.objects.get(pk=items['manuInventory'])
        except Exception as e:
            print(e)
            bdacct.ppeProperty = None
        try:
            bdacct.ppePlant = AccountChild.objects.get(pk=items['ppePlant'])
        except Exception as e:
            print(e)
            bdacct.ppePlant = None
        try:
            bdacct.ppeEquipment = AccountChild.objects.get(pk=items['ppeEquipment'])
        except Exception as e:
            print(e)
            bdacct.ppeEquipment = None
        try:
            bdacct.inputVat = AccountChild.objects.get(pk=items['inputVat'])
        except Exception as e:
            print(e)
            bdacct.inputVat = None
        try:
            bdacct.outputVat = AccountChild.objects.get(pk=items['outputVat'])
        except Exception as e:
            print(e)
            bdacct.outputVat = None
        try:
            bdacct.ewp = AccountChild.objects.get(pk=items['ewp'])
        except Exception as e:
            print(e)
            bdacct.ewp = None
        try:
            bdacct.sales = AccountChild.objects.get(pk=items['sales'])
        except Exception as e:
            print(e)
            bdacct.sales = None
        try:
            bdacct.costOfSales = AccountChild.objects.get(pk=items['costOfSales'])
        except Exception as e:
            print(e)
            bdacct.costOfSales = None
        try:
            bdacct.otherIncome = AccountChild.objects.get(pk=items['otherIncome'])
        except Exception as e: 
            print(e)
            bdacct.otherIncome = None
        try:
            bdacct.cwit = AccountChild.objects.get(pk=items['cwit'])
        except Exception as e:
            print(e)
            bdacct.cwit = None

        for item in items['cashInBank']:
            bdacct.cashInBank.add(AccountChild.objects.get(pk=item))

        for item in items['advancesToSupplier']:
            bdacct.advancesToSupplier = AccountChild.objects.get(pk=item)
        
        bdacct.save()
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class BranchesView(View):
    def get(self, request, format=None):
        return render(request, 'branches.html')