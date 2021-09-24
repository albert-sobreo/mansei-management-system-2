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

class CompletionReportView(View):
    def get(self, request):
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
        cr.spareParts = ReceivingReport.objects.get(pk=crJson['spareParts'])
        cr.damagePhoto = request.FILES['damagePhoto']
        cr.recommendation = crJson['recommendation']
        
        cr.save()
        request.user.branch.completionReport.add(cr)

        for po in crJson['crpo']:
            crpo = CRPO()
            crpo.cr = cr
            crpo.purchaseOrder = PurchaseOrder.objects.get(pk=po['purchaseOrder'])
            crpo.save()
            request.user.branch.crpo.add(crpo)

        for rr in crJson['crSpareParts']:
            crsp = CRSpareParts()
            crsp.cr = cr
            crsp.receivingReport = ReceivingReport.objects.get(pk=po['receivingReport'])
            crsp.save()
            request.user.branch.crSpareParts.add(crsp)

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)

class CRList(View):
    def get(self, request):
        return render(request, 'cr-list.html')