import sweetify
from decimal import Decimal
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from ..forms import *
from ..models import *
from datetime import date as now
from datetime import datetime
from datetime import timedelta
from .journalAPI import jeAPI, voidJournal
from django.core.exceptions import PermissionDenied
from .notificationCreate import *

class JournalView(View):
    def get(self, request):
        if request.user.authLevel == '2':
            return redirect('/purchase-request/')

        user = request.user

        try:
            startDate = request.GET['startDate']
            endDate = request.GET['endDate']
        
        except:
            startDate = now(now.today().year, 1,1)
            try:
                nextMonth = now.today().replace(month=now.today().replace(day=1).month+1, day=1)
            except Exception as e:
                print(e)
                nextMonth = now.today().replace(month=1, day=1)
            print(nextMonth)
            endDate = nextMonth - timedelta(days=1)

        try:
            j = user.branch.journal.filter(code__regex=r'J-')
            j = j.latest('pk')
            listed_code = j.code.split('-')
            listed_date = str(now.today()).split('-')

            current_code = int(listed_code[3])
            
            if listed_code[1] == listed_date[0] and listed_code[2] == listed_date[1]:
                current_code += 1
                new_code = 'J-{}-{}-{}'.format(listed_date[0], listed_date[1], str(current_code).zfill(4))
            else:
                new_code = 'J-{}-{}-0001'.format(listed_date[0], listed_date[1])

        except Exception as e:
            print(e)
            listed_date = str(now.today()).split('-')
            new_code = 'J-{}-{}-0001'.format(listed_date[0], listed_date[1])


        print(startDate, endDate)
        context = {
            'new_code': new_code,
            'journals': request.user.branch.journal.filter(journalDate__range=[startDate, endDate]).order_by('pk').reverse(),
            'startDate': startDate,
            'endDate': endDate
        }


        
        return render(request, 'journal.html', context)

class SaveJournal(APIView):
    def post(self, request, format=None):
        if request.user.authLevel == '2':
            raise PermissionDenied()
        print(request.data)

        print(request.data['date'])

        journal = request.data
        debit = request.data['debit']
        credit = request.data['credit']

        j = Journal()

        j.code = journal['code']
        if journal['retroactive']:
            j.journalDate = journal['retroactive']
        else:
            j.journalDate = journal['date']
        j.remarks = journal['remarks']
        j.datetimeCreated = datetime.now()
        j.createdBy = User.objects.get(pk=request.session.get('_auth_user_id'))

        j.save()
        
        request.user.branch.journal.add(j)

        for item in debit:
            jeAPI(request, j, item['normally'], AccountChild.objects.get(pk=(item['accountChild'])), Decimal(item['amount']))

        for item in credit:
            jeAPI(request, j, item['normally'], AccountChild.objects.get(pk=(item['accountChild'])), Decimal(item['amount']))
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)
        
class VoidJournal(View):
    def post(self, request, pk):
        journal = Journal.objects.get(pk=pk)
        voidJournal(request, journal)
        
        sweetify.sweetalert(request, icon='success', title='Success!', persistent='Dismiss')
        return JsonResponse(0, safe=False)