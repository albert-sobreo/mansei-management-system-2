import sweetify
from decimal import Decimal
from django import views
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from ..forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from ..models import *
import json
from datetime import date as now
from datetime import datetime
from .journalAPI import jeAPI

class JournalView(View):
    def get(self, request):

        user = request.user

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

        context = {
            'new_code': new_code,
            'journals': request.user.branch.journal.all().order_by('datetimeCreated').reverse()
        }
        return render(request, 'journal.html', context)

class SaveJournal(APIView):
    def post(self, request, format=None):
        print(request.data)

        print(request.data['date'])

        journal = request.data
        debit = request.data['debit']
        credit = request.data['credit']

        j = Journal()

        j.code = journal['code']
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
        