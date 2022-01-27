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

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)