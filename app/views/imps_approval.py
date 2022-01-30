from rest_framework.views import APIView
from ..models import *
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
import sweetify
from decimal import Decimal
from datetime import datetime
import re
from .journalAPI import jeAPI
from .petty_cash_api import *
from django.core.exceptions import PermissionDenied

class JobOrdernonapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        context = {
            'jos': request.user.branch.jobOrder.filter(approved = False)
        }
        return render(request, 'job-order-nonapproved.html', context)

class JobOrderapproved(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()

        context = {
            'jos': request.user.branch.jobOrder.filter(approved=True)
        }

        return render(request, 'job-order-approved.html', context)

class JobOrderApprovalAPI(APIView):
    def post(self, request):
        if request.user.authLevel == '2' or request.user.authLevel == '1':
            raise PermissionDenied()
        jo = JobOrder.objects.get(pk=request.data['id'])

        dChildAccount = request.user.branch.branchProfile.branchDefaultChildAccount

        jo.datetimeApproved = datetime.datetime.now()
        jo.approved = True
        jo.approvedBy = request.user
        jo.status = 'on-going'

        jo.save()

        rawmat = Decimal(0)
        for material in jo.rawmaterials.all():
            rawmat += material.totalCost
        
        overhead = Decimal(0)
        for oh in jo.overheadexpenses.all():
            overhead += oh.cost

        labor = Decimal (0)
        for work in jo.directlabor.all():
            labor += work.cost

        j = Journal()

        j.code = jo.code
        j.datetimeCreated = jo.datetimeCreated
        j.createdBy = jo.createdBy
        j.journalDate = datetime.now()
        j.save()
        request.user.branch.journal.add(j)
        
        if not rawmat == Decimal(0):
            jeAPI(request, j, 'Credit', dChildAccount.inventory, rawmat)
        if not overhead == Decimal(0):
            jeAPI(request, j, 'Credit', dChildAccount.factorySupplies, overhead)
        if not labor == Decimal(0):
            jeAPI(request, j, 'Credit', dChildAccount.laborExpense, labor)

        jeAPI(request, j, 'Debit', dChildAccount.workInProgress, rawmat+overhead+labor)



        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)