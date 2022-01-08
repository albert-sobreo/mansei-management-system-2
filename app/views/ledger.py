from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from ..models import *
from datetime import date as now
from datetime import timedelta
from django.core.exceptions import PermissionDenied

class LedgerView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        
        except:
            startDate = now.today().replace(day=1)
            try:
                nextMonth = now.today().replace(month=startDate.month+1, day=1)
            except:
                nextMonth = now.today().replace(month=1, day=1)
            endDate = nextMonth - timedelta(days=1)

        context = {
            'children': request.user.branch.accountChild.all().order_by('pk'),
            'startDate': startDate,
            'endDate': endDate,
            'date': str(startDate)+ ',' +str(endDate),
            'pos': request.user.branch.purchaseOrder.all().order_by('pk').iterator()
        }
        return render(request, 'ledger.html', context)