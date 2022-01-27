from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
import datetime
from django.core.exceptions import PermissionDenied

class JobOrderView(View):
    def get(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()

        user = request.user

        try:
            jo = user.branch.jobOrder.latest('pk')

            listed_code = jo.code.split('-')
            listed_date = str(datetime.date.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'JO-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'JO-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(datetime.date.today()).split('-')
            new_code = 'JO-{}-{}-0001'.format(listed_date[0], listed_date[1])

        operationalExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Oo]peration")
        administrativeExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Aa]dmin")
        context = {
            'new_code': new_code,
            'operational': operationalExpenses,
            'administrative': administrativeExpenses
        }    
        return render(request, 'job-order.html', context)

class CreateJobOrderAPI(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        jo = JobOrder()

        jo.code = request.data['code']
        jo.datetimeCreated = datetime.datetime.now()
        jo.jobOrderCost = request.data['jobOrderCost']
        jo.method = request.data['method']
        jo.save()
        request.user.branch.jobOrder.add(jo)

        if request.user.is_authenticated:
            jo.createdBy = request.user
            jo.save()

        for item in request.data['rawmaterials']:
            if item['merchInventory']:
                rawMat = RawMaterials()
                rawMat.merchInventory = MerchandiseInventory.objects.get(pk=item['merchInventory'])
                rawMat.jobOrder = jo
                rawMat.qty = item['qty']
                rawMat.remaining = item['remaining']
                rawMat.purchasingPrice = item['purchasingPrice']
                rawMat.totalCost = item['totalCost']
                rawMat.save()
                request.user.branch.rawMaterials.add(rawMat)

        for item in request.data['overheadexpenses']:
            if item['expenses']:
                ov = OverheadExpenses()
                ov.expenses = AccountChild.objects.get(pk=item['expenses'])
                ov.cost = item['cost']
                ov.jobOrder = jo
                ov.save()
                request.user.branch.overheadExpenses.add(ov)

        for item in request.data['finalproduct']:
            if item['name']:
                finalProduct = FinalProduct()
                finalProduct.name = item['name']
                finalProduct.qty = item['qty']
                finalProduct.unitCost = item['unitCost']
                finalProduct.totalCost = item['totalCost']
                finalProduct.jobOrder = jo
                finalProduct.save()
                request.user.branch.finalProduct.add(finalProduct)

        for item in request.data['materiallosses']:
            if item['name']:
                losses = MaterialLosses()
                losses.name = item['name']
                losses.qty = item['qty']
                losses.unitCost = item['unitCost']
                losses.totalCost = item['totalCost']
                losses.jobOrder = jo
                losses.save()
                request.user.branch.materialLosses.add(losses)
        

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

        

class JobOrderOnGoingView(View):
    def get(self, request):
        context = {
            'jos': request.user.branch.jobOrder.filter(status='on-going')
        }
        return render(request, 'job-order-ongoing.html', context)

class JobOrderFinishedView(View):
    def get(self, request):
        context = {
            'jos': request.user.branch.jobOrder.filter(status='finished')
        }
        return render(request, 'job-order-finished.html', context)

class EditJobOrderView(View):
    def get(self, request):
        if request.user.authLevel=='2':
            raise PermissionDenied()


        operationalExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Oo]peration")
        administrativeExpenses = request.user.branch.accountGroup.filter(name__regex=r"[Aa]dmin")


        context = {
            'jos': request.user.branch.jobOrder.exclude(status='finished'),
            'operational': operationalExpenses,
            'administrative': administrativeExpenses
        }

        return render(request, 'job-order-edit-on-going.html', context)

class EditJobOrder(APIView):
    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        jo = JobOrder.objects.get(pk=request.data['id'])

        jo.rawmaterials.all().delete()
        jo.overheadexpenses.all().delete()
        jo.finalproduct.all().delete()
        jo.materiallosses.all().delete()

        jo.save()

        for item in request.data['rawmaterials']:
            if item['merchInventory']:
                rawMat = RawMaterials()
                rawMat.merchInventory = MerchandiseInventory.objects.get(pk=item['merchInventory'])
                rawMat.jobOrder = jo
                rawMat.qty = item['qty']
                rawMat.remaining = item['remaining']
                rawMat.purchasingPrice = item['purchasingPrice']
                rawMat.totalCost = item['totalCost']
                rawMat.save()
                request.user.branch.rawMaterials.add(rawMat)

        for item in request.data['overheadexpenses']:
            if item['expenses']:
                ov = OverheadExpenses()
                ov.expenses = AccountChild.objects.get(pk=item['expenses'])
                ov.cost = item['cost']
                ov.jobOrder = jo
                ov.save()
                request.user.branch.overheadExpenses.add(ov)

        for item in request.data['finalproduct']:
            if item['name']:
                finalProduct = FinalProduct()
                finalProduct.name = item['name']
                finalProduct.qty = item['qty']
                finalProduct.unitCost = item['unitCost']
                finalProduct.totalCost = item['totalCost']
                finalProduct.jobOrder = jo
                finalProduct.save()
                request.user.branch.finalProduct.add(finalProduct)

        for item in request.data['materiallosses']:
            if item['name']:
                losses = MaterialLosses()
                losses.name = item['name']
                losses.qty = item['qty']
                losses.unitCost = item['unitCost']
                losses.totalCost = item['totalCost']
                losses.jobOrder = jo
                losses.save()
                request.user.branch.materialLosses.add(losses)
        
        jo.jobOrderCost = request.data['jobOrderCost']
        jo.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class JobOrderFinish(APIView):
    def post(self, request, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        jo = JobOrder.objects.get(pk=request.data['id'])
        jo.datatimeFinished = datetime.datetime.now()
        jo.status = 'finished'
        jo.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

        