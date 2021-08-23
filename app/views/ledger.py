from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from ..forms import *
from ..models import *
from datetime import date as now
from datetime import timedelta

class LedgerView(View):
    def get(self, request):
        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        
        except:
            startDate = now.today().replace(day=1)
            nextMonth = now.today().replace(month=startDate.month+1, day=1)
            endDate = nextMonth - timedelta(days=1)

        context = {
            'children': request.user.branch.accountChild.all(),
            'startDate': startDate,
            'endDate': endDate,
            'date': str(startDate)+ ',' +str(endDate)
        }
        return render(request, 'ledger.html', context)