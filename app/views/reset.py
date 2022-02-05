
from decimal import Decimal
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *
import sweetify
from .notificationCreate import *

class ResetChartOfAccounts(View):
    def get(self, request):
        return render(request, 'reset-accounts.html')

class ResetChartOfAccountsProcess(APIView):
    def post(self, request):
        p = request.data

        if p['proceed']:
            for group in request.user.branch.accountGroup.all():
                group.amount = Decimal(0)
                group.save()

                for sub in group.accountsubgroup.all():
                    sub.amount = Decimal(0)
                    sub.save()

                    for child in sub.accountchild.all():
                        child.amount = Decimal(0)
                        child.save()

        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)