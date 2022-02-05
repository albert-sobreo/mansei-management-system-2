from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from rest_framework.views import APIView
from ..serializers import *
from ..models import *
import sweetify
from datetime import date as now
from decimal import Decimal
from datetime import datetime
import json
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class CompletionReportView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
            
        user = request.user

        try:
            cr = user.branch.completionReport.latest('pk')

            listed_code = cr.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])

            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = "CR-{}-{}-{}".format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = "CR-{}-{}-0001".format(listed_date[0], listed_date[1])

        except Exception as e:
            listed_date = str(now.today()).split('-')
            new_code = "CR-{}-{}-0001".format(listed_date[0], listed_date[1])

        context = {
            "new_code": new_code,
        }
        return render(request, 'completion-report.html', context)

    def post(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        print(request.FILES)
        print(request.POST)
        print(request.POST['postDATA'])
        print()
        crJson = json.loads(request.POST['postDATA'])
        print(crJson['code'])
        print(crJson['reportDate'])

        cr = CompletionReport()
        cr.code = crJson['code']
        cr.datetimeCreated = datetime.now()
        cr.createdBy = request.user
        cr.reportDate = crJson['reportDate']
        cr.ppe = PPE.objects.get(pk=crJson['ppe'])
        cr.malfuncDate = crJson['malfuncDate']
        cr.damageDescription = crJson['damageDescription']
        cr.damagePhoto = request.FILES['damagePhoto']
        cr.recommendation = crJson['recommendation']
        cr.totalCost = crJson['totalCost']
        
        cr.save()
        request.user.branch.completionReport.add(cr)

        for po in crJson['crpo']:
            crpo = CRPO()
            crpo.cr = cr
            crpo.purchaseOrder = PurchaseOrder.objects.get(pk=po['purchaseOrder'])
            crpo.save()
            request.user.branch.crpo.add(crpo)

        for rr in crJson['crspareparts']:
            crsp = CRSpareParts()
            crsp.cr = cr
            crsp.receivingReport = ReceivingReport.objects.get(pk=rr['receivingReport'])
            crsp.save()
            request.user.branch.crSpareParts.add(crsp)

        notify(request, 'New Completion Report', cr.code, '/cr-nonapproved/', 1)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class CRList(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        return render(request, 'cr-list.html')

class CRSuccessUpdate(APIView):
    def put(self, request, pk, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        cr = CompletionReport.objects.get(pk=pk)
        cr.successPhoto = request.FILES['successPhoto']
        cr.status = 'Success'
        cr.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class CRIncompleteUpdate(APIView):
    def put(self, request, pk, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        crJson = request.data

        cr = CompletionReport.objects.get(pk=pk)
        cr.status = 'Incomplete'
        cr.reason = crJson['reason']
        cr.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class CRTransactionUpdate(APIView):
    def put(self, request, pk, format = None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        
        crJson = request.data

        cr = CompletionReport.objects.get(pk=pk)
        
        for po in crJson['crpo']:
            crpo = CRPO()
            crpo.cr = cr
            crpo.purchaseOrder = PurchaseOrder.objects.get(pk=po['purchaseOrder'])
            crpo.save()
            request.user.branch.crpo.add(crpo)

        for rr in crJson['crspareparts']:
            crsp = CRSpareParts()
            crsp.cr = cr
            crsp.receivingReport = ReceivingReport.objects.get(pk=rr['receivingReport'])
            crsp.save()
            request.user.branch.crSpareParts.add(crsp)

        cr.totalCost += Decimal(crJson['totalCost'])
        cr.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class CRCapitalize(APIView):
    def put(self, request, pk):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        cr = CompletionReport.objects.get(pk=pk)
        cr.ppe.bookValue += cr.totalCost
        NUMERATOR = cr.ppe.bookValue * cr.ppe.deprCycle
        DENOMINATOR = int(cr.ppe.usefulLife * 12) - int(cr.ppe.accumDepr // cr.ppe.deprRate)
        cr.ppe.deprRate = Decimal(NUMERATOR)/Decimal(DENOMINATOR)
        cr.capitalized = True
        cr.ppe.save()
        cr.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

